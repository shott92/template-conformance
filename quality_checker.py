import re

# List of weak/vague words that indicate lack of Specificity/Measurability
WEAK_WORDS = {
    'fast', 'slow', 'easy', 'difficult', 'user-friendly', 'robust', 'seamless', 
    'state-of-the-art', 'minimal', 'maximal', 'approx', 'approximately', 'about', 
    'enough', 'sufficient', 'adequate', 'quickly', 'efficiently'
}

# List of words indicating incompleteness
PLACEHOLDERS = {'tbd', 'tbc', 'todo', '<value>', '...'}

class QualityAnalyzer:
    def __init__(self, text, system_response=None):
        self.text = text
        self.system_response = system_response # Just the system response part, for Atomicity check
        self.issues = []

    def analyze(self):
        self._check_specific_measurable()
        self._check_atomic()
        self._check_sufficient()
        return self.issues

    def _check_specific_measurable(self):
        # Check for weak words
        # Update regex to include hyphens in words
        words = re.findall(r'\b[\w-]+\b', self.text.lower())
        found_weak = [w for w in words if w in WEAK_WORDS]
        if found_weak:
            self.issues.append(f"Vague words found (Not Specific/Measurable): {', '.join(set(found_weak))}")

    def _check_atomic(self):
        # If we have the system response separated, check it for conjunctions
        if self.system_response:
            # Simple check for 'and', 'or', 'as well as' in the system response
            # This is a heuristic; 'and' can be valid in a list of objects "display X and Y"
            # but often indicates compound requirements "do X and do Y".
            # For strict atomicity, we flag it.
            if re.search(r'\b(and|or|as well as)\b', self.system_response.lower()):
                self.issues.append("Conjunction found in System Response (Possibly not Atomic)")
        elif re.search(r'\b(and|or|as well as)\b', self.text.lower()):
             # Fallback if no system response extraction
             pass 

    def _check_sufficient(self):
        # Check for placeholders
        words = re.findall(r'\b\w+\b', self.text.lower())
        found_placeholders = [w for w in words if w in PLACEHOLDERS]
        if '<value>' in self.text.lower() or '...' in self.text:
             found_placeholders.append("placeholder")
             
        if found_placeholders:
            self.issues.append(f"Placeholders found (Not Sufficient): {', '.join(set(found_placeholders))}")
