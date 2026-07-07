from dataclasses import dataclass, field
from pathlib import Path
import yaml
import os
import re

VERSION_PATTERN = re.compile(r"^v(\d+)\.yaml$")

@dataclass
class PromptSpec:
    name: str
    version: str
    description: str
    author: str
    model: str
    params: dict
    template: str
    system: str = ""
    source_path: Path = field(default=None, repr=False)


class PromptLoader:
    def __init__(self, prompts_dir):
        self.prompts_dir = Path(prompts_dir)

    def _version_numbers(self,prompt_dir):
        versions = []
        for yaml_file in prompt_dir.glob("v*.yaml"):
            match = VERSION_PATTERN.match(yaml_file.name)
            if match:
                versions.append(int(match.group(1)))        
        versions.sort()
        return versions
                

    def load(self,name,version=None):
        prompt_dir = self.prompts_dir / name
        if not os.path.exists(prompt_dir):
            raise FileNotFoundError(f"Prompt {name} not found") 

        versions = self._version_numbers(prompt_dir)
    
        if version==None:
            version = versions[-1]        
        
        filename = f"v{version}.yaml"

        yaml_file = prompt_dir / filename      
        
        if not os.path.exists(yaml_file):
            raise FileNotFoundError(f"Prompt {name} with version {version} not found")
    
        with open(yaml_file) as r:
            prompt_data = yaml.safe_load(r)
        
        return PromptSpec(
            name=prompt_data["name"],
            version=str(prompt_data["version"]),
            description=prompt_data.get("description", ""),
            author=prompt_data.get("author", ""),
            model=prompt_data.get("model", "claude-sonnet-4-6"),
            params=prompt_data.get("params", {}),
            system=prompt_data.get("system", ""),
            template=prompt_data["template"],
            source_path=yaml_file,
        )


    def list_prompts(self) -> list[dict]:
        """
        Iterate over every subdirectory in prompts_dir and collect version information.

        Returns:
            [
                {
                    "name": "invoice",
                    "versions": ["1", "2", "10"],
                    "latest": "10"
                },
                ...
            ]
        """        
        results = []

        for prompt_dir in self.prompts_dir.iterdir():
            if not prompt_dir.is_dir():
                continue

            versions = []

            for yaml_file in prompt_dir.glob("v*.yaml"):
                match = VERSION_PATTERN.match(yaml_file.name)
                if match:
                    versions.append(int(match.group(1)))

            if not versions:
                continue

            versions.sort()

            results.append(
                {
                    "name": prompt_dir.name,
                    "versions": [str(v) for v in versions],
                    "latest": str(versions[-1]),
                }
            )

        return results

    def history(self,name):
        prompt_dir = self.prompts_dir / name
        if not prompt_dir.exists():
          raise FileNotFoundError(f"Prompt '{name}' not found")
        prompts = []            
        versions = self._version_numbers(prompt_dir)        
        for version in versions:
            prompt_spec = self.load(name,version)
            prompts.append(prompt_spec)
        return prompts

if __name__ == "__main__":
    prompt_loader = PromptLoader("../../phase-1-prompt-mgmt/prompts/")
    prompt = prompt_loader.load("ticket_classifier")
    print(prompt)