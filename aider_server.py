from flask import Flask, request, jsonify
import argparse
from api.code_assistant import CodeAssistantAPI

app = Flask(__name__)
code_assistant = CodeAssistantAPI()

@app.route('/code_assistant', methods=['POST'])
def handle_code_assistant():
    data = request.get_json()
    
    if not data or 'instruction' not in data:
        return jsonify({'error': 'Instruction is required'}), 400
    
    try:
        instruction = data['instruction']
        files = data.get('files', [])
        directory = data.get('directory', None)
        model = data.get('model', None)
        options = data.get('options', {})
        
        response = code_assistant.execute_instruction(
            instruction=instruction,
            files=files,
            directory=directory,
            model=model,
            options=options
        )
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/klue', methods=['POST'])
def klue():
    # Read the JSON payload from the request body
    data = request.get_json()

    # Log the parsed data for debugging
    # print("Parsed data:", data)

    # Validate the payload structure
    if not data or "data" not in data or "aider" not in data["data"]:
        print("Invalid payload format")
        return jsonify({'error': 'Invalid payload format'}), 400

    try:
        # Extract values from the payload
        aider = data["data"]["aider"]
        rules = aider.get("rules", {})
        
        dry_run = rules.get("dry_run", {}).get("p1", False)
        instruction = rules.get("instruction", {}).get("p1", "Default Instruction")

        # Handle directory and model logic
        directory = rules.get("directory", {}).get("p1")
        directory = None if directory == "default" else directory

        model = rules.get("model", {}).get("p1")
        model = None if model == "default" else model

        confirm = rules.get("confirm", {}).get("p1", False)

        # Log the extracted values
        print("Dry Run:", dry_run)
        print("Instruction:", instruction)
        print("Directory:", directory)
        print("Model:", model)
        print("Confirm:", confirm)

        # Navigate to the files
        process_data = data["data"].get("process-data", {})
        file_collector = process_data.get("file_collector-1", {})
        file_collector_data = file_collector.get("data", {})
        files_content = file_collector_data.get("files", {}).get("content", [])

        # Extract file paths
        files = [item.get("file") for item in files_content if "file" in item]
        print("Files to be processed:", files)

        # If dry run, return a mock response without execution
        if dry_run:
            print("Dry run enabled. Skipping execution.")
            return jsonify({
                'response': 'Dry run completed successfully',
                'dry_run': dry_run,
                'instruction': instruction,
                'directory': directory,
                'model': model,
                'confirm': confirm,
                'files': files
            }), 200

        # Execute the instruction
        options = {
            'confirm': confirm
        }

        response = code_assistant.execute_instruction(
            instruction=instruction,
            files=files,
            directory=directory,
            model=model,
            options=options
        )

        # Return the execution result
        return jsonify({'response': response}), 200
    except Exception as e:
        print("Error processing data:", str(e))
        return jsonify({'error': str(e)}), 500

def main():
    parser = argparse.ArgumentParser(description='Aider Web API Server')
    parser.add_argument('--port', type=int, default=5000,
                       help='Port to run the server on (default: 5000)')
    args = parser.parse_args()
    
    app.run(port=args.port)

if __name__ == '__main__':
    main()
