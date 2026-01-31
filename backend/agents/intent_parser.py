import re
from typing import Dict, Any, List, Tuple
from enum import Enum

from .base import BaseAgent
from ..utils.logging import setup_logging

logger = setup_logging()


class IntentType(Enum):
    """
    Enum representing different types of user intents in the todo system.
    """
    ADD_TASK = "ADD_TASK"
    VIEW_TASKS = "VIEW_TASKS"
    COMPLETE_TASK = "COMPLETE_TASK"
    UPDATE_TASK = "UPDATE_TASK"
    DELETE_TASK = "DELETE_TASK"
    SET_RECURRING = "SET_RECURRING"
    UNKNOWN = "UNKNOWN"


class IntentParserAgent(BaseAgent):
    """
    Agent responsible for parsing user input to identify intent and extract entities.
    """
    
    def __init__(self):
        super().__init__("IntentParserAgent")
        
        # Define patterns for different intents
        self.patterns = {
            IntentType.ADD_TASK: [
                # English patterns
                r"(add|create|make|new)\s+(a\s+|an\s+|the\s+)?(task|todo|to-do|item)\s+(.+)",
                r"(add|create|make|new)\s+(.+)\s+(as\s+a\s+task|to\s+my\s+list|to\s+do)",
                r"(remind\s+me\s+to|need\s+to|want\s+to)\s+(.+)",
                r"(.+)\s+(remind\s+me|task|todo)",
                r"(add|create|make|new)\s+(.+)",  # Simple add command

                # Roman Urdu patterns
                r"(task|kaam|kam|work)\s+(add|shamil|dal|daal|add karo|kar do|kardo|krdo|kr dou|krdou|krdun|krdin|krdiyen)\s+(.+)",
                r"(task|kaam|kam|work)\s+(ban|bnay|banaye|create|create karo|banao|bnayen|bnaye)\s+(.+)",
                r"(yaad|yad|yaad dilao|remind)\s+(karo|karwana|krwana|kar do|kardo|krdo|kr dou|krdou|krdun|krdin|krdiyen)\s+(.+)",
                r"(mera|meri|my)\s+(task|kaam|kam|work)\s+(add|shamil|dal|daal|kar do|kardo|krdo|kr dou|krdou)\s+(.+)",
                r"(mera|meri|my)\s+(task|kaam|kam|work)\s+(add|shamil|dal|daal|kar do|kardo|krdo|kr dou|krdou)\s+(.+)\s+(karna|karni|karna hai|karni hai)",
                r"(mujhe|mjhe|menhe|ko|kko|koe)\s+(.+)\s+(leni|lena|leni hai|karni|karna|chaiye|chahiye)\s+(.+)?",
                r"(.+)\s+(add|kar|karo|do|dou|kardo|krdo|krdou)\s+(mera|meri|my)\s+(task|kaam|kam|work)",
            ],
            IntentType.VIEW_TASKS: [
                # English patterns
                r"(show|list|display|view|see|get|fetch)\s+(my\s+)?(tasks|todos|to-dos|items|list)",
                r"(what|which)\s+(do\s+i\s+have|am\s+i\s+supposed\s+to\s+do|are\s+my\s+tasks)",
                r"my\s+(tasks|todos|to-dos)",
                r"(check|review)\s+(my\s+)?(tasks|todos)",
                r"(all|everything|my)\s+(tasks|todos)",  # Show all tasks

                # Roman Urdu patterns
                r"(show|dikha|dikhao|dikhaw|dekh|dekhao|dekho|show karo)\s+(my|mera|mere|meri)\s+(tasks|kaam|kam|works|list|lst)",
                r"(kya\s+kya\s+hai|konsa\s+konsa\s+kaam\s+hai|what|kya|kye)\s+(mera|meri|my)\s+(task|kaam|kam|work)",
                r"(mera|meri|my)\s+(task|kaam|kam|work)\s+(list|lst|list karo|list dikha|list dikhao)",
                r"(sab|sb|all|sara|saray|sari)\s+(tasks|kaam|kam|works|list|lst)",
            ],
            IntentType.COMPLETE_TASK: [
                # English patterns
                r"(complete|finish|done|mark.*complete|check|tick|accomplish)\s+(a\s+|an\s+|the\s+)?(task|todo|to-do|item|it)\s*(.+)?",
                r"(mark|set)\s+(a\s+|an\s+|the\s+)?(task|todo|to-do|item)\s+(as\s+)?(complete|done|finished)",
                r"(.+)\s+(is\s+done|is\s+complete|is\s+finished|done|complete)",
                r"(complete|finish|done|mark)\s+(.+)",  # Simple complete command

                # Roman Urdu patterns
                r"(complete|ho\s+gya|hogya|ho\s+gye|hogye|done|khatam|khtm|finish|mkml|mukammal|poora|poori)\s+(.+)",
                r"(mark|naksh|nishan|nishaan|nishaan lag|mark karo)\s+(as\s+)?(complete|done|ho\s+gya|hogya|khatam|finish)",
                r"(mera|meri|my)\s+(task|kaam|kam|work)\s+(complete|ho\s+gya|hogya|done|khatam|finish)\s+(.+)",
                r"(kar\s+dio|kar dio|kardo|krdo|kr dio|done|complete)\s+(mera|meri|my)\s+(task|kaam|kam|work)",
            ],
            IntentType.UPDATE_TASK: [
                # English patterns
                r"(update|change|modify|edit|alter)\s+(a\s+|an\s+|the\s+)?(task|todo|to-do|item)\s+(.+)",
                r"(change|update|modify)\s+(.+)",
                r"(rename|retitle)\s+(.+)",

                # Roman Urdu patterns
                r"(update|badlo|badal|updte|bartan|bartan karo|tazah|tazah karo)\s+(.+)",
                r"(change|badlo|badal|chg|bartan|bartan karo)\s+(.+)",
                r"(mera|meri|my)\s+(task|kaam|kam|work)\s+(update|badlo|badal|chg|bartan|tazah)\s+(.+)",
                r"(modify|edit|mufta|mufta karo|taraqi|taraqi de|tarqi de)\s+(.+)",
            ],
            IntentType.DELETE_TASK: [
                # English patterns
                r"(delete|remove|kill|trash|eliminate)\s+(a\s+|an\s+|the\s+)?(task|todo|to-do|item)\s*(.+)?",
                r"(remove|delete)\s+(.+)",

                # Roman Urdu patterns
                r"(delete|mita|mita do|mitado|mita|remove|htao|hatao|hata|delete karo)\s+(.+)",
                r"(remove|htao|hatao|hata|nikalo|nikal|delete|mita)\s+(.+)",
                r"(mera|meri|my)\s+(task|kaam|kam|work)\s+(delete|mita|remove|htao|hatao)\s+(.+)",
                r"(kill|khatam|khtm|khatam karo|khtm karo)\s+(.+)",
            ],
            IntentType.SET_RECURRING: [
                # English patterns
                r"(set|make|configure)\s+(a\s+|an\s+|the\s+)?(task|todo|to-do|item)\s+to\s+repeat|recur|cycle",
                r"(.+)\s+(daily|weekly|monthly|every\s+day|every\s+week|every\s+month)",
                r"repeat|recurring|recurrent",

                # Roman Urdu patterns
                r"(repeat|dohra|dohrana|dohray|doobara|dobara|dobray|bar\s+bar|barbar|recurring|recurrent)\s+(.+)",
                r"(daily|har\s+roz|hr\s+roz|rozana|roz\s+roz|har\s+day|hr\s+day|daily)\s+(.+)",
                r"(weekly|har\s+hafta|hr\s+hafta|hafta\s+war|haftawar|har\s+week|hr\s+week|weekly)\s+(.+)",
                r"(monthly|har\s+mahina|hr\s+mahina|mahina\s+war|mahinawar|har\s+month|hr\s+month|monthly)\s+(.+)",
            ]
        }
        
        # Define entity extraction patterns
        self.entity_patterns = {
            "task_title": [
                # English patterns
                r"(?:to|that|is|for|about)\s+(?P<title>[^.!?]+?)(?:\s+(?:as|in|on|at)\s+|$|[.!?])",
                r"(?:add|create|make|new|remind me to|need to|want to)\s+(?P<title>[^.!?]+?)(?:\s+(?:as|in|on|at)\s+|$|[.!?])",

                # Roman Urdu patterns
                r"(?:task|kaam|kam|work)\s+(?:add|shamil|dal|daal|ban|bnay|banaye|create)\s+(?P<title>[^.!?]+?)(?:\s+(?:ki|ke|ka|par|per)\s+|$|[.!?])",
                r"(?:mera|meri|my)\s+(?:task|kaam|kam|work)\s+(?:update|badlo|badal|change|chg|bartan|tazah)\s+(?P<title>[^.!?]+?)(?:\s+(?:ki|ke|ka|par|per)\s+|$|[.!?])",
                r"(?:karo|krwana|krwana|kar|kr|karna|kro)\s+(?P<title>[^.!?]+?)(?:\s+(?:ki|ke|ka|par|per)\s+|$|[.!?])",
                r"(?:mujhe|muj ko|mujhe|mjhe|mj ko)\s+(?P<title>[^.!?]+?)\s+(?:leni|lena|leni hai|karni|karna)\s+(?:hai|he|hy|ho|raha hai|rahi hai)",
            ],
            "task_id": [
                # English patterns
                r"(task|number|id)\s+(\d+)",
                r"#(\d+)",

                # Roman Urdu patterns
                r"(task|kaam|kam|work|nmbr|number|id)\s+(\d+)",
                r"(\d+)\s+(?:ka|ke|ki)\s+(?:task|kaam|kam|work)",
            ],
            "priority": [
                # English patterns
                r"(priority|high|higher|low|lower|medium|importance)\s+(?P<priority>\d|[1-5]|high|higher|low|lower|medium)",
                r"(important|very|critical|urgent)",

                # Roman Urdu patterns
                r"(aoliyat|aulawi|awli|awliyat|priority|zaida|ziada|zaida|ziada|kam|km|less|zarrori|zaroori|zruri|zaruri|zaroori|zarrori)\s+(?P<priority>\d|[1-5]|high|higher|low|lower|medium|aoli|aula|zaida|ziada|kam|km|zarrori|zaroori|zruri)",
            ],
            "due_date": [
                # English patterns
                r"(by|on|before|deadline|due)\s+(?P<date>\w+\s+\d{1,2}(?:st|nd|rd|th)?(?:,\s*\d{4})?|\d{1,2}/\d{1,2}(?:/\d{4})?|\d{4}-\d{2}-\d{2})",
                r"(today|tomorrow|tonight|this week|next week|this weekend|monday|tuesday|wednesday|thursday|friday|saturday|sunday)",

                # Roman Urdu patterns
                r"(tab|jb|jab|tk|taak|tak|due|last date|last din|akhri|akri|last|final|khatam|khtm)\s+(?P<date>\w+\s+\d{1,2}(?:st|nd|rd|th)?(?:,\s*\d{4})?|\d{1,2}/\d{1,2}(?:/\d{4})?|\d{4}-\d{2}-\d{2}|aaj|kal|raat|iss week|agla week|iss hafte|agle hafte|iss saal|agle saal|monday|tuesday|wednesday|thursday|friday|saturday|sunday|somvar|mangalvar|budhvar|guruvar|shukrvar|shanivar|ravivar)",
            ],
            "recurrence": [
                # English patterns
                r"(daily|weekly|monthly|every day|every week|every month)",

                # Roman Urdu patterns
                r"(daily|har\s+roz|hr\s+roz|rozana|roz\s+roz|har\s+day|hr\s+day|har roz|hr roz|daily)",
                r"(weekly|har\s+hafta|hr\s+hafta|hafta\s+war|haftawar|har\s+week|hr\s+week|har hafta|hr hafta|weekly)",
                r"(monthly|har\s+mahina|hr\s+mahina|mahina\s+war|mahinawar|har\s+month|hr\s+month|har mahina|hr mahina|monthly)",
            ]
        }
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse the user input to identify intent and extract entities.
        
        Args:
            context: Dictionary containing 'user_input' key with the user's message
            
        Returns:
            Dictionary with 'intent' and 'entities' keys
        """
        user_input = context.get("user_input", "").strip().lower()
        
        if not user_input:
            return {
                "intent": IntentType.UNKNOWN.value,
                "confidence": 0.0,
                "entities": {},
                "original_input": context.get("user_input", "")
            }
        
        # Detect intent
        intent, confidence = self._detect_intent(user_input)
        
        # Extract entities
        entities = self._extract_entities(user_input, intent)
        
        # Detect language
        language = self.detect_language(user_input)

        # Log the execution
        self.log_execution(
            context={"user_input": user_input, "intent": intent.value, "confidence": confidence, "language": language},
            result={"entities": entities}
        )

        return {
            "intent": intent.value,
            "confidence": confidence,
            "entities": entities,
            "language": language,
            "original_input": context.get("user_input", "")
        }
    
    def _detect_intent(self, user_input: str) -> Tuple[IntentType, float]:
        """
        Detect the intent from the user input.
        
        Args:
            user_input: The user's input string
            
        Returns:
            Tuple of (detected intent, confidence score)
        """
        best_intent = IntentType.UNKNOWN
        best_confidence = 0.0
        
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    # Calculate confidence based on pattern match
                    confidence = min(0.9, 0.5 + (len(pattern) / 100))
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_intent = intent
        
        # If no pattern matched but we have a clear indication, assign intent with lower confidence
        if best_intent == IntentType.UNKNOWN:
            # Check for keywords that might indicate intent
            if any(word in user_input for word in ["add", "create", "new", "remind me to"]):
                best_intent = IntentType.ADD_TASK
                best_confidence = 0.6
            elif any(word in user_input for word in ["show", "list", "view", "see", "what"]):
                best_intent = IntentType.VIEW_TASKS
                best_confidence = 0.6
            elif any(word in user_input for word in ["complete", "done", "finish", "mark"]):
                best_intent = IntentType.COMPLETE_TASK
                best_confidence = 0.6
            elif any(word in user_input for word in ["update", "change", "modify", "edit"]):
                best_intent = IntentType.UPDATE_TASK
                best_confidence = 0.6
            elif any(word in user_input for word in ["delete", "remove", "kill", "trash"]):
                best_intent = IntentType.DELETE_TASK
                best_confidence = 0.6
            elif any(word in user_input for word in ["repeat", "daily", "weekly", "monthly"]):
                best_intent = IntentType.SET_RECURRING
                best_confidence = 0.6
        
        return best_intent, best_confidence

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text.

        Args:
            text: The input text to analyze

        Returns:
            Detected language code ('en' for English, 'ur' for Urdu, 'rom_ur' for Roman Urdu)
        """
        # Urdu uses Arabic script, so we check for Arabic/Urdu characters
        urdu_regex = re.compile(r'[\u0600-\u06FF\u0750-\u077F]')

        # Check for Roman Urdu keywords
        roman_urdu_keywords = [
            'mera', 'meri', 'meray', 'tumhara', 'tumhari', 'tumhare', 'humara', 'humari', 'humare',
            'kya', 'kyun', 'kab', 'kahan', 'kaise', 'kim', 'kaun', 'kon',
            'hai', 'hain', 'tha', 'thi', 'they', 'hogya', 'hogye', 'hoga', 'hogi',
            'main', 'tum', 'wo', 'ye', 'vo', 'hum', 'aap', 'ham',
            'ka', 'ke', 'ki', 'kae', 'kay', 'gee', 'ga', 'gi', 'raha', 'rahi', 'rahe', 'tha', 'thi', 'the',
            'aur', 'or', 'lekin', 'magar', 'lakin', 'par', 'per', 'kay', 'ke', 'ker', 'kar', 'karo', 'krdo', 'krdio',
            'task', 'kaam', 'kam', 'work', 'naam', 'ism', 'nam',
            'aaj', 'kal', 'raat', 'din', 'roz', 'subah', 'shaam',
            'haan', 'nahi', 'ji', 'han', 'ji han', 'ji haan', 'bilkul', 'jaroor', 'zaroor',
            'shukriya', 'dhanyawaad', 'thank you', 'thanks', 'meherbani', 'madad', 'help',
            'bura', 'accha', 'aala', 'buland', 'neeche', 'upar', 'agee', 'peeche', 'center', 'bich',
            'din', 'mahina', 'saal', 'time', 'waqt', 'date', 'tarikh'
        ]

        if urdu_regex.search(text):
            return 'ur'
        elif any(keyword in text.lower() for keyword in roman_urdu_keywords):
            # Additional check: if it's mostly Latin characters with Roman Urdu keywords, it's Roman Urdu
            latin_chars = sum(1 for c in text if c.isalpha() and ord(c) < 128)
            total_chars = sum(1 for c in text if c.isalpha())

            if total_chars > 0 and latin_chars / total_chars > 0.7:  # If more than 70% are Latin characters
                return 'rom_ur'
            else:
                return 'en'
        else:
            return 'en'

    def _extract_entities(self, user_input: str, intent: IntentType) -> Dict[str, Any]:
        """
        Extract entities from the user input based on the detected intent.
        
        Args:
            user_input: The user's input string
            intent: The detected intent
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {}
        
        # Extract task title
        for pattern in self.entity_patterns["task_title"]:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                title = match.group("title") if "title" in match.groupdict() else match.group(0)
                # Clean up the title
                title = re.sub(r"(to|that|is|for|about)\s+", "", title, flags=re.IGNORECASE).strip()
                if title:
                    entities["task_title"] = title
                    break
        
        # Extract task ID
        for pattern in self.entity_patterns["task_id"]:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                task_id = match.group(1) if len(match.groups()) > 1 else match.group(0)
                entities["task_id"] = task_id
                break
        
        # Extract priority
        for pattern in self.entity_patterns["priority"]:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                priority_text = match.group(0)
                if "high" in priority_text or "higher" in priority_text or "important" in priority_text or "very" in priority_text or "critical" in priority_text or "urgent" in priority_text:
                    entities["priority"] = 1  # High priority
                elif "low" in priority_text or "lower" in priority_text:
                    entities["priority"] = 5  # Low priority
                elif "medium" in priority_text:
                    entities["priority"] = 3  # Medium priority
                else:
                    # Try to extract numeric priority
                    num_match = re.search(r"\d", priority_text)
                    if num_match:
                        num = int(num_match.group(0))
                        if 1 <= num <= 5:
                            entities["priority"] = num
                break
        
        # Extract due date
        for pattern in self.entity_patterns["due_date"]:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                date_text = match.group("date") if "date" in match.groupdict() else match.group(0)
                entities["due_date"] = date_text.strip()
                break
        
        # Extract recurrence
        for pattern in self.entity_patterns["recurrence"]:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                recurrence_text = match.group(0)
                if "daily" in recurrence_text or "every day" in recurrence_text:
                    entities["recurrence"] = "daily"
                elif "weekly" in recurrence_text or "every week" in recurrence_text:
                    entities["recurrence"] = "weekly"
                elif "monthly" in recurrence_text or "every month" in recurrence_text:
                    entities["recurrence"] = "monthly"
                break
        
        # Special handling based on intent
        if intent == IntentType.COMPLETE_TASK and "task_title" in entities and "task_id" not in entities:
            # If user wants to complete a task by title, we might need to look it up
            entities["lookup_by_title"] = True

        # Special handling for ADD_TASK
        if intent == IntentType.ADD_TASK:
            # If no task title was extracted but we detected an ADD_TASK intent,
            # try to extract the task title from the entire user input
            if "task_title" not in entities:
                # Look for content after common verbs in English and Roman Urdu
                verbs = ["add", "create", "make", "new", "remind me to", "need to", "want to",
                         "task add", "task shamil", "task dal", "task daal", "task ban",
                         "kaam add", "kaam shamil", "kaam dal", "kaam daal", "kaam ban",
                         "kam add", "kam shamil", "kam dal", "kam daal", "kam ban",
                         "work add", "work create", "yaad kar", "yaad dilao", "mera task add"]

                for verb in verbs:
                    if verb in user_input:
                        # Extract everything after the verb
                        parts = user_input.split(verb, 1)
                        if len(parts) > 1:
                            potential_title = parts[1].strip()
                            # Clean up the title
                            potential_title = potential_title.replace("a task", "").replace("a to-do", "").replace("a todo", "").replace("an item", "").replace("the task", "").strip()
                            potential_title = potential_title.replace("mera", "").replace("meri", "").replace("ka", "").replace("ki", "").replace("ko", "").strip()
                            if potential_title and len(potential_title) > 1:
                                entities["task_title"] = potential_title
                                break

                # If still no title, try to extract from Roman Urdu patterns like "mujhe sabzi leni he"
                if "task_title" not in entities:
                    # Look for patterns like "mujhe [task] leni hai/he"
                    import re
                    pattern = r"(?:mujhe|muj ko|mujhe|mjhe|mj ko)\s+(.*?)\s+(?:leni|lena|leni hai|karni|karna)\s+(?:hai|he|hy|ho|raha hai|rahi hai)"
                    match = re.search(pattern, user_input.lower())
                    if match:
                        potential_title = match.group(1).strip()
                        if potential_title and len(potential_title) > 1:
                            entities["task_title"] = potential_title

        # Special handling for UPDATE_TASK
        if intent == IntentType.UPDATE_TASK:
            # Extract what specifically needs to be updated
            if "task_title" in user_input and ("update" in user_input or "change" in user_input or "badlo" in user_input or "badal" in user_input or "bartan" in user_input or "tazah" in user_input):
                entities["update_field"] = "title"
            elif "priority" in user_input or "important" in user_input or "aoliyat" in user_input or "zarrori" in user_input or "zaroori" in user_input:
                entities["update_field"] = "priority"
            elif "due date" in user_input or "deadline" in user_input or "tab tk" in user_input or "jb tk" in user_input:
                entities["update_field"] = "due_date"

        # Special handling for DELETE_TASK
        if intent == IntentType.DELETE_TASK and "task_title" in entities and "task_id" not in entities:
            entities["lookup_by_title_for_deletion"] = True

        # Special handling for SET_RECURRING
        if intent == IntentType.SET_RECURRING:
            if "daily" in user_input or "every day" in user_input or "har roz" in user_input or "hr roz" in user_input or "rozana" in user_input:
                entities["recurrence"] = "daily"
            elif "weekly" in user_input or "every week" in user_input or "har hafta" in user_input or "hr hafta" in user_input or "haftawar" in user_input:
                entities["recurrence"] = "weekly"
            elif "monthly" in user_input or "every month" in user_input or "har mahina" in user_input or "hr mahina" in user_input or "mahinawar" in user_input:
                entities["recurrence"] = "monthly"

        return entities


# Convenience function to create and run the agent
async def parse_intent(user_input: str) -> Dict[str, Any]:
    """
    Convenience function to parse intent from user input.
    
    Args:
        user_input: The user's input string
        
    Returns:
        Dictionary with intent and entities
    """
    agent = IntentParserAgent()
    return await agent.execute({"user_input": user_input})