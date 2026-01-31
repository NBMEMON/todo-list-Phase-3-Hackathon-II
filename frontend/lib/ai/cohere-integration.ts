'use client';

// Environment variable for Cohere API key
const COHERE_API_KEY = process.env.NEXT_PUBLIC_COHERE_API_KEY;

export interface CohereResponse {
  id: string;
  generations: Array<{
    id: string;
    text: string;
  }>;
  prompt: string;
}

export interface CohereEmbeddingResponse {
  id: string;
  embeddings: number[][];
}

export class CohereAPI {
  private static readonly BASE_URL = 'https://api.cohere.ai/v1';
  
  /**
   * Generates text using Cohere's generate endpoint
   * @param prompt The input prompt for text generation
   * @param maxTokens Maximum number of tokens to generate
   * @returns Generated text response
   */
  static async generate(prompt: string, maxTokens: number = 100): Promise<CohereResponse> {
    if (!COHERE_API_KEY) {
      throw new Error('Cohere API key is not configured. Please set NEXT_PUBLIC_COHERE_API_KEY in your environment variables.');
    }

    try {
      const response = await fetch(`${this.BASE_URL}/generate`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${COHERE_API_KEY}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          model: 'command',
          prompt: prompt,
          max_tokens: maxTokens,
          temperature: 0.7,
          k: 0,
          p: 0.9,
          frequency_penalty: 0,
          presence_penalty: 0,
          stop_sequences: [],
          return_likelihoods: 'NONE'
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Cohere API error: ${response.status} - ${errorData.message || 'Unknown error'}`);
      }

      const data = await response.json();
      return data as CohereResponse;
    } catch (error) {
      console.error('Error calling Cohere API:', error);
      throw error;
    }
  }

  /**
   * Generates embeddings using Cohere's embed endpoint
   * @param texts Array of texts to generate embeddings for
   * @returns Embeddings response
   */
  static async embed(texts: string[]): Promise<CohereEmbeddingResponse> {
    if (!COHERE_API_KEY) {
      throw new Error('Cohere API key is not configured. Please set NEXT_PUBLIC_COHERE_API_KEY in your environment variables.');
    }

    try {
      const response = await fetch(`${this.BASE_URL}/embed`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${COHERE_API_KEY}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          model: 'embed-english-v3.0',
          texts: texts,
          input_type: 'search_query'
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Cohere API error: ${response.status} - ${errorData.message || 'Unknown error'}`);
      }

      const data = await response.json();
      return data as CohereEmbeddingResponse;
    } catch (error) {
      console.error('Error calling Cohere embed API:', error);
      throw error;
    }
  }

  /**
   * Classifies text using Cohere's classify endpoint
   * @param inputs Array of texts to classify
   * @param examples Array of example classifications
   * @returns Classification response
   */
  static async classify(inputs: string[], examples: Array<{text: string, label: string}>): Promise<any> {
    if (!COHERE_API_KEY) {
      throw new Error('Cohere API key is not configured. Please set NEXT_PUBLIC_COHERE_API_KEY in your environment variables.');
    }

    try {
      const response = await fetch(`${this.BASE_URL}/classify`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${COHERE_API_KEY}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          model: 'large',
          inputs: inputs,
          examples: examples
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Cohere API error: ${response.status} - ${errorData.message || 'Unknown error'}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error calling Cohere classify API:', error);
      throw error;
    }
  }
}

// Enhanced intent classification using Cohere
export class EnhancedIntentClassifier {
  /**
   * Classifies user intent using Cohere's classification API
   * @param userInput The user's natural language input
   * @returns Classified intent
   */
  static async classifyIntent(userInput: string): Promise<string> {
    // Define intent examples for classification
    const examples = [
      // Create task examples
      { text: "Add a task to buy groceries", label: "CREATE_TASK" },
      { text: "Create a reminder to call mom", label: "CREATE_TASK" },
      { text: "Make a new task to finish report", label: "CREATE_TASK" },
      { text: "Add task: walk the dog", label: "CREATE_TASK" },
      
      // Update task examples
      { text: "Change the title of my first task", label: "UPDATE_TASK" },
      { text: "Update my meeting task to tomorrow", label: "UPDATE_TASK" },
      { text: "Modify the grocery task", label: "UPDATE_TASK" },
      { text: "Edit the description of task 3", label: "UPDATE_TASK" },
      
      // Delete task examples
      { text: "Remove the old task", label: "DELETE_TASK" },
      { text: "Delete the first task", label: "DELETE_TASK" },
      { text: "Get rid of that task", label: "DELETE_TASK" },
      { text: "Trash the meeting reminder", label: "DELETE_TASK" },
      
      // Complete task examples
      { text: "Mark the grocery task as done", label: "COMPLETE_TASK" },
      { text: "Finish the report task", label: "COMPLETE_TASK" },
      { text: "Check off the exercise task", label: "COMPLETE_TASK" },
      { text: "Complete the laundry task", label: "COMPLETE_TASK" },
      
      // List tasks examples
      { text: "Show me my tasks", label: "LIST_TASKS" },
      { text: "What do I have to do today?", label: "LIST_TASKS" },
      { text: "Display my to-do list", label: "LIST_TASKS" },
      { text: "What are my tasks?", label: "LIST_TASKS" },
      
      // Search tasks examples
      { text: "Find tasks about meeting", label: "SEARCH_TASKS" },
      { text: "Look for grocery tasks", label: "SEARCH_TASKS" },
      { text: "Search for urgent tasks", label: "SEARCH_TASKS" },
      { text: "Find the report task", label: "SEARCH_TASKS" }
    ];

    try {
      const result = await CohereAPI.classify([userInput], examples);
      
      if (result && result.classifications && result.classifications.length > 0) {
        const classification = result.classifications[0];
        return classification.prediction;
      }
      
      // Fallback to rule-based classification if API fails
      return 'UNKNOWN';
    } catch (error) {
      console.error('Error with Cohere classification:', error);
      // Fallback to rule-based classification
      return 'UNKNOWN';
    }
  }

  /**
   * Generates a more natural response using Cohere's generation API
   * @param userInput The user's input
   * @param context Context about the operation performed
   * @returns Generated natural response
   */
  static async generateNaturalResponse(userInput: string, context: string): Promise<string> {
    const prompt = `
      User input: "${userInput}"
      Operation performed: "${context}"
      
      Generate a natural, friendly response acknowledging the user's request and the operation performed.
      Keep the response concise but warm and helpful.
      If the operation had an error, acknowledge it in a helpful way.
      Respond in the same language as the user's input if possible.
    `;

    try {
      const response = await CohereAPI.generate(prompt, 100);
      return response.generations[0]?.text?.trim() || context;
    } catch (error) {
      console.error('Error generating natural response:', error);
      // Fallback to simple context return
      return context;
    }
  }
}