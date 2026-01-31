'use client';

// Intent types
export enum IntentType {
  CREATE_TASK = 'CREATE_TASK',
  UPDATE_TASK = 'UPDATE_TASK',
  DELETE_TASK = 'DELETE_TASK',
  COMPLETE_TASK = 'COMPLETE_TASK',
  LIST_TASKS = 'LIST_TASKS',
  SEARCH_TASKS = 'SEARCH_TASKS',
  UNKNOWN = 'UNKNOWN'
}

// Entity extraction result
export interface EntityResult {
  title?: string;
  description?: string;
  taskId?: string;
  completed?: boolean;
  priority?: number;
  searchQuery?: string;
}

// Parsed intent result
export interface IntentResult {
  intent: IntentType;
  entities: EntityResult;
  confidence: number;
}

// Intent patterns for matching
const INTENT_PATTERNS = {
  [IntentType.CREATE_TASK]: [
    /\b(add|create|make|new)\s+(a\s+|an\s+|the\s+)?(task|todo|to-do|item)\b/i,
    /\b(want\s+to\s+|need\s+to\s+|should\s+|will)\s+(add|create|make)\b/i,
    /\b(remind\s+me\s+to|don't\s+forget\s+to)\b/i
  ],
  [IntentType.UPDATE_TASK]: [
    /\b(update|change|modify|edit)\s+(a\s+|an\s+|the\s+)?(task|todo|to-do|item)\b/i,
    /\b(change\s+(title|description|priority)|update\s+(title|description|priority))\b/i
  ],
  [IntentType.DELETE_TASK]: [
    /\b(delete|remove|kill|trash)\s+(a\s+|an\s+|the\s+)?(task|todo|to-do|item)\b/i,
    /\b(remove\s+this|delete\s+this)\b/i
  ],
  [IntentType.COMPLETE_TASK]: [
    /\b(complete|finish|done|mark.*complete|check|tick)\s+(a\s+|an\s+|the\s+)?(task|todo|to-do|item)\b/i,
    /\b(mark.*as\s+(done|completed|finished))\b/i,
    /\b(done\s+with|finished\s+with)\b/i
  ],
  [IntentType.LIST_TASKS]: [
    /\b(list|show|display|view|see|get)\s+(my\s+)?(tasks|todos|to-dos|items)\b/i,
    /\b(what.*have|what.*need|what.*to\s+do)\b/i,
    /\b(my\s+)?(tasks|todos|to-dos)\b/i
  ],
  [IntentType.SEARCH_TASKS]: [
    /\b(find|look\s+for|search|locate)\s+(a\s+|an\s+|the\s+)?(task|todo|to-do|item)\b/i,
    /\b(where.*is|where.*are)\b/i
  ]
};

// Entity extraction patterns
const ENTITY_PATTERNS = {
  title: /(?:to\s+|for\s+|that\s+|is\s+)"?([^".]+)"?/,
  description: /(?:description|desc|note):\s*(.+)/i,
  taskId: /(?:task\s+id|id|number)\s*(\d+)/i,
  priority: /(?:priority|high|medium|low|prio)\s*(\d|[1-5])/i,
  searchQuery: /(?:for|about|regarding)\s+(.+)/i
};

export class IntentParserAgent {
  /**
   * Parses user input to determine intent and extract entities
   * @param input The user's natural language input
   * @returns Parsed intent and extracted entities
   */
  static async parseIntent(input: string): Promise<IntentResult> {
    // Normalize input
    const normalizedInput = input.trim().toLowerCase();
    
    // Find the best matching intent
    let bestMatch: {
      intent: IntentType;
      confidence: number;
    } | null = null;
    
    for (const [intent, patterns] of Object.entries(INTENT_PATTERNS)) {
      for (const pattern of patterns) {
        if (pattern.test(normalizedInput)) {
          const confidence = this.calculateConfidence(pattern, normalizedInput);
          
          if (!bestMatch || confidence > bestMatch.confidence) {
            bestMatch = {
              intent: intent as IntentType,
              confidence
            };
          }
        }
      }
    }
    
    // If no intent matched, return unknown
    if (!bestMatch) {
      return {
        intent: IntentType.UNKNOWN,
        entities: {},
        confidence: 1.0
      };
    }
    
    // Extract entities based on the detected intent
    const entities = this.extractEntities(input, bestMatch.intent);
    
    return {
      intent: bestMatch.intent,
      entities,
      confidence: bestMatch.confidence
    };
  }
  
  /**
   * Calculates confidence score for a pattern match
   * @param pattern The regex pattern that matched
   * @param input The user input
   * @returns Confidence score between 0 and 1
   */
  private static calculateConfidence(pattern: RegExp, input: string): number {
    // Simple confidence calculation based on pattern complexity and match length
    const matches = input.match(pattern);
    if (!matches) return 0;
    
    // More specific patterns get higher confidence
    const patternComplexity = pattern.toString().length;
    const matchLength = matches[0].length;
    
    // Normalize to 0-1 range
    return Math.min(1.0, (matchLength * patternComplexity) / 1000);
  }
  
  /**
   * Extracts entities from the input based on the detected intent
   * @param input The user input
   * @param intent The detected intent
   * @returns Extracted entities
   */
  private static extractEntities(input: string, intent: IntentType): EntityResult {
    const entities: EntityResult = {};
    
    // Extract title
    const titleMatch = input.match(ENTITY_PATTERNS.title);
    if (titleMatch && titleMatch[1]) {
      entities.title = titleMatch[1].trim();
    }
    
    // Extract description
    const descMatch = input.match(ENTITY_PATTERNS.description);
    if (descMatch && descMatch[1]) {
      entities.description = descMatch[1].trim();
    }
    
    // Extract task ID
    const idMatch = input.match(ENTITY_PATTERNS.taskId);
    if (idMatch && idMatch[1]) {
      entities.taskId = idMatch[1].trim();
    }
    
    // Extract priority
    const priorityMatch = input.match(ENTITY_PATTERNS.priority);
    if (priorityMatch && priorityMatch[1]) {
      const priorityNum = parseInt(priorityMatch[1], 10);
      if (!isNaN(priorityNum) && priorityNum >= 1 && priorityNum <= 5) {
        entities.priority = priorityNum;
      }
    }
    
    // Extract search query
    const searchMatch = input.match(ENTITY_PATTERNS.searchQuery);
    if (searchMatch && searchMatch[1]) {
      entities.searchQuery = searchMatch[1].trim();
    }
    
    // Special handling based on intent
    switch (intent) {
      case IntentType.COMPLETE_TASK:
        // Look for completion indicators
        if (/(complete|done|finish)/i.test(input)) {
          entities.completed = true;
        } else if (/(incomplete|not done|not finished)/i.test(input)) {
          entities.completed = false;
        } else {
          // Default to true for completion intent
          entities.completed = true;
        }
        break;
        
      case IntentType.CREATE_TASK:
        // If we have a title but no description, try to use the rest of the input
        if (entities.title && !entities.description) {
          const titleIndex = input.toLowerCase().indexOf(entities.title.toLowerCase());
          if (titleIndex !== -1) {
            const afterTitle = input.substring(titleIndex + entities.title.length).trim();
            if (afterTitle && !afterTitle.startsWith('"')) {
              entities.description = afterTitle;
            }
          }
        }
        break;
    }
    
    return entities;
  }
  
  /**
   * Determines if the input is in Urdu
   * @param input The user input
   * @returns True if the input is in Urdu, false otherwise
   */
  static isUrdu(input: string): boolean {
    // Urdu uses Arabic script, so we check for Arabic/Urdu characters
    const urduRegex = /[\u0600-\u06FF\u0750-\u077F]/;
    return urduRegex.test(input);
  }
}