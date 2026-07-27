"""Closed execution interface for named project-native policy commands."""

from __future__ import annotations

from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]
SUPPORTED_TOOLS = {"just"}


def command_for(commands: JsonObject, command_id: str) -> tuple[list[str], float]:
    raw_commands = commands.get("commands")
    if not isinstance(raw_commands, dict) or command_id not in raw_commands:
        raise ValueError(f"unknown policy command id: {command_id}")
    specification = raw_commands[command_id]
    if not isinstance(specification, dict):
        raise ValueError(f"policy command {command_id} must be an object")
    tool = specification.get("tool")
    binary = specification.get("binary")
    arguments = specification.get("arguments")
    additional = specification.get("additional_arguments")
    timeout = specification.get("timeout_seconds")
    if tool not in SUPPORTED_TOOLS:
        raise ValueError(f"policy command {command_id} uses unsupported tool {tool}")
    if not isinstance(binary, str) or not binary:
        raise ValueError(f"policy command {command_id} needs a binary")
    if Path(binary).name != tool:
        raise ValueError(f"policy command {command_id} binary does not match tool {tool}")
    if not isinstance(arguments, list) or not all(
        isinstance(value, str) and value for value in arguments
    ):
        raise ValueError(f"policy command {command_id} needs arguments")
    if not isinstance(additional, list) or not all(isinstance(value, str) for value in additional):
        raise ValueError(f"policy command {command_id} has invalid additional arguments")
    if not isinstance(timeout, (int, float)) or not 1 <= timeout <= 3600:
        raise ValueError(f"policy command {command_id} has an invalid timeout")
    return [binary, *arguments, *additional], float(timeout)
