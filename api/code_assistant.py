from aider.coders import Coder
from aider.models import Model
import os

class CodeAssistantAPI:
    def __init__(self):
        self.current_coder = None
    
    def execute_instruction(self, instruction, files=None, directory=None, model=None, options=None):
        """
        Execute an instruction using Aider
        
        Args:
            instruction (str): The instruction to execute
            files (list): Optional list of files to operate on
            directory (str): Optional working directory
            model (str): Optional model specification
            options (dict): Optional configuration options
        
        Returns:
            str: Response from the execution
        """
        if directory:
            original_dir = os.getcwd()
            os.chdir(directory)
        
        try:
            # Initialize model
            model_instance = Model(model if model else "gpt-4-turbo")
            
            # Set up files list
            fnames = files if files else []
            
            # Create new coder instance
            self.current_coder = Coder.create(
                main_model=model_instance,
                fnames=fnames
            )
            
            # Configure options if provided
            if options:
                if 'auto_commits' in options:
                    self.current_coder.auto_commits = options['auto_commits']
                if 'dirty_commits' in options:
                    self.current_coder.dirty_commits = options['dirty_commits']
                if 'dry_run' in options:
                    self.current_coder.dry_run = options['dry_run']
            
            # Execute the instruction
            response = self.current_coder.run(instruction)
            
            return response if response else "Instruction executed successfully"
            
        finally:
            if directory:
                os.chdir(original_dir)
