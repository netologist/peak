import click
import os
import sys

@click.group()
def cli():
    """FastAPI Laravel CLI tool"""
    pass

@cli.command()
@click.argument('name')
def make_controller(name):
    """Create a new controller"""
    template = f"""
from .base_controller import BaseController

class {name.capitalize()}Controller(BaseController):
    def __init__(self):
        super().__init__()
        self.setup_routes()

    def setup_routes(self):
        self.router.get("/{name.lower()}", tags=["{name.lower()}"])(self.index)

    async def index(self):
        return {{"message": "{name} index"}}
"""
    with open(f"app/controllers/{name.lower()}_controller.py", "w") as f:
        f.write(template.strip())
    click.echo(f"Controller {name} created successfully")

@cli.command()
@click.argument('name')
def make_model(name):
    """Create a new model"""
    template = f"""
from sqlalchemy import Column, String
from .base import BaseModel

class {name.capitalize()}(BaseModel):
    __tablename__ = "{name.lower()}s"
    
    name = Column(String)
    description = Column(String, nullable=True)
"""
    with open(f"app/models/{name.lower()}.py", "w") as f:
        f.write(template.strip())
    click.echo(f"Model {name} created successfully")

if __name__ == '__main__':
    cli()