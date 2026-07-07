import click
from dotenv import load_dotenv
from shared.prompt_manager import PromptLoader, LLMClient, render_prompt, compare_versions
import json
from pathlib import Path

DEFAULT_PROMPTS_DIR = str(Path(__file__).resolve().parents[1] / "prompts")

@click.group()
@click.option(
                "--prompt-dir",
                default=DEFAULT_PROMPTS_DIR,
                show_default=True,
                type=click.Path(exists=True, file_okay=False),
            )
@click.pass_context
def cli(ctx,prompt_dir):
    load_dotenv()
    ctx.ensure_object(dict)
    loader = PromptLoader(prompt_dir)
    ctx.obj["loader"] = loader    

@cli.command("list")
@click.pass_context
def list_prompts(ctx):
    print(ctx.obj['loader'].list_prompts())

@cli.command()
@click.argument("name",required=True)
@click.pass_context
def show(ctx,name):    
    prompt_spec = ctx.obj['loader'].load(name)    
    print(prompt_spec)

@cli.command()
@click.argument("name",required=True)
@click.option("--vars",required=True)
@click.pass_context
def run(ctx,name,vars):        
    vars = json.loads(vars)    
    prompt_spec = ctx.obj['loader'].load(name)
    system, user = render_prompt(prompt_spec,vars)
    llm_client = LLMClient()
    response = llm_client.run(prompt_spec,system,user)
    print(response)    

@cli.command()
@click.argument("name",required=True)
@click.option("--v1",required=True)
@click.option("--v2",required=True)
@click.option("--vars",required=True)
@click.pass_context
def diff(ctx,name,v1,v2,vars):
    llm_client = LLMClient()
    vars = json.loads(vars)
    results = compare_versions(ctx.obj['loader'], llm_client, name, v1, v2, vars)
    print(results)

@cli.command()
@click.pass_context
@click.argument("name",required=True)
def history(ctx,name):    
    print(ctx.obj['loader'].history(name))


if __name__ == "__main__":
    from dotenv import load_dotenv
    from shared.prompt_manager.loader import PromptLoader, PromptSpec
    from shared.prompt_manager.renderer import render_prompt
    from shared.prompt_manager.client import LLMClient
    from shared.prompt_manager.diff import compare_versions
    load_dotenv()
    cli(obj={})