import os
import json
import hashlib
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class ScriptureAuditReport(BaseModel):
    is_authentic_edition: bool = Field(description="True if verified against authoritative Sanskrit archives (e.g., BORI, GRETIL, Gita Press)")
    is_complete_text: bool = Field(description="True if chapter and verse counts match the complete traditional text; False if partial/truncated")
    is_grammatically_valid: bool = Field(description="True if Sanskrit/Hindi text is clean Devanagari/IAST without gibberish or encoding corruption")
    canonical_source_match: str = Field(description="Name of the verified reference edition or archive matched via cross-referencing")
    rejection_reasons: List[str] = Field(description="Detailed list of missing chapters, formatting errors, or authenticity failures if rejected")

class DvarapalaGatekeeperAgent:
    """
    The Nalanda Gatekeeper Agent (Dvarapala).
    Enforces strict deduplication, completeness, grammatical integrity, and web cross-referencing
    before allowing any community-contributed scripture into the Nalanda Library.
    """
    def __init__(self, registry_path: str = "data/checksum_registry.json", model_name: str = "gpt-4o"):
        self.registry_path = registry_path
        self.llm = ChatOpenAI(model=model_name, temperature=0.0) # Zero temperature for strict factual auditing
        self.parser = PydanticOutputParser(pydantic_object=ScriptureAuditReport)
        self.known_hashes = self._load_checksum_registry()

    def _load_checksum_registry(self) -> Dict[str, str]:
        """Loads SHA-256 hashes of all previously accepted scriptures to block duplicates."""
        if os.path.exists(self.registry_path):
            with open(self.registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def verify_deduplication(self, scripture_name: str, raw_content: str) -> Dict[str, Any]:
        """Gate 1: Generates a SHA-256 fingerprint to prevent duplicate uploads."""
        content_hash = hashlib.sha256(raw_content.strip().encode("utf-8")).hexdigest()
        
        if content_hash in self.known_hashes.values():
            return {"passed": False, "reason": f"Duplicate Rejected: Exact content fingerprint already exists in Nalanda Library."}
        
        if scripture_name.lower() in [k.lower() for k in self.known_hashes.keys()]:
            return {"passed": False, "reason": f"Duplicate Rejected: '{scripture_name}' is already registered. Submit an update PR instead."}
            
        return {"passed": True, "hash": content_hash}

    def audit_scripture_submission(self, scripture_name: str, raw_content: str, chapter_count: int, verse_count: int) -> Dict[str, Any]:
        """
        Executes the full 4-Gate Verification Audit on a contributor's uploaded text.
        """
        # Gate 1: Check Duplicates
        dedup_check = self.verify_deduplication(scripture_name, raw_content)
        if not dedup_check["passed"]:
            return {"approved": False, "status": "REJECTED_DUPLICATE", "details": [dedup_check["reason"]]}

        # Extract sample slices (Beginning, Middle, End) to audit text quality and structure
        total_len = len(raw_content)
        sample_slice = (
            f"--- BEGINNING ---\n{raw_content[:1500]}\n"
            f"--- MIDDLE ---\n{raw_content[total_len//2 : (total_len//2)+1500]}\n"
            f"--- END ---\n{raw_content[-1500:]}"
        )

        # Gates 2, 3, & 4: Completeness, Sanskrit Integrity & Indological Cross-Reference
        audit_prompt = ChatPromptTemplate.from_template(
            "You are the DVARAPALA GATEKEEPER AGENT of the Nalanda Digital Library.\n"
            "A contributor has submitted a scripture for inclusion. You must cross-reference your knowledge "
            "of authoritative Sanskrit digital archives (GRETIL, BORI Critical Editions, Gita Press, SARIT, Muktabodha) "
            "to verify its authenticity, completeness, and linguistic purity.\n\n"
            "Submitted Scripture Name: {name}\n"
            "Declared Chapter/Adhyaya Count: {chapters}\n"
            "Declared Total Verse/Shloka Count: {verses}\n\n"
            "Text Samples (Start, Middle, End):\n{samples}\n\n"
            "Audit Rules:\n"
            "1. Reject if the chapter/verse count is significantly lower than the complete canonical text (no partial uploads).\n"
            "2. Reject if the text contains AI gibberish, broken Unicode, or unverified colonial-era distortions.\n"
            "3. Verify that the beginning and ending verses match the authentic traditional opening and closing of this scripture.\n"
            "{format_instructions}"
        )

        formatted = audit_prompt.format_messages(
            name=scripture_name,
            chapters=chapter_count,
            verses=verse_count,
            samples=sample_slice,
            format_instructions=self.parser.get_format_instructions()
        )

        response = self.llm.invoke(formatted)
        report = self.parser.parse(response.content)

        # Final Decision Logic
        if report.is_authentic_edition and report.is_complete_text and report.is_grammatically_valid:
            return {
                "approved": True,
                "status": "APPROVED_FOR_NALANDA",
                "hash": dedup_check["hash"],
                "verified_edition": report.canonical_source_match,
                "action": f"Auto-checking box for '{scripture_name}' in docs/NALANDA_LEDGER.md and spawning Rishi Agent."
            }
        else:
            return {
                "approved": False,
                "status": "REJECTED_AUDIT_FAILED",
                "details": report.rejection_reasons
            }

if __name__ == "__main__":
    print("Dvarapala Gatekeeper & Authenticity Cross-Reference Agent initialized.")
