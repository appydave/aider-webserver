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

def main():
    parser = argparse.ArgumentParser(description='Aider Web API Server')
    parser.add_argument('--port', type=int, default=5000,
                       help='Port to run the server on (default: 5000)')
    args = parser.parse_args()
    
    app.run(port=args.port)

if __name__ == '__main__':
    main()
