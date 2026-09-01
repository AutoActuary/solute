// SOLUTE-MANAGED: native hot-path hook. Remove with `codex plugin remove solute@solute`.

use serde_json::{Value, json};
use std::env;
use std::error::Error;
use std::fs;
use std::io::{self, Write};
use std::path::PathBuf;

fn is_sol_model(model: &str) -> bool {
    let slug = model.trim().to_ascii_lowercase();
    slug == "sol" || slug.ends_with("-sol") || slug.contains("-sol-")
}

fn opted_out(prompt: &str) -> bool {
    let prompt = prompt.to_ascii_lowercase();
    [
        "don't use solute",
        "don't use /solute",
        "don't use $solute",
        "do not use solute",
        "do not use /solute",
        "do not use $solute",
    ]
    .iter()
    .any(|phrase| prompt.contains(phrase))
}

fn should_activate(event: &Value) -> bool {
    event.get("hook_event_name").and_then(Value::as_str) == Some("UserPromptSubmit")
        && event
            .get("model")
            .and_then(Value::as_str)
            .is_some_and(is_sol_model)
        && !event
            .get("prompt")
            .and_then(Value::as_str)
            .is_some_and(opted_out)
}

fn plugin_root() -> Result<PathBuf, Box<dyn Error>> {
    if let Some(root) = env::var_os("PLUGIN_ROOT") {
        return Ok(PathBuf::from(root));
    }
    let executable = env::current_exe()?;
    Ok(executable
        .parent()
        .and_then(|bin| bin.parent())
        .ok_or("cannot resolve plugin root")?
        .to_path_buf())
}

fn load_policy() -> Result<String, Box<dyn Error>> {
    let references = plugin_root()?
        .join("skills")
        .join("solute")
        .join("references");
    let policy = fs::read_to_string(references.join("policy.md"))?;
    let guide = references.join("delegation-guide.md");
    Ok(policy
        .trim()
        .replace("`delegation-guide.md`", &format!("`{}`", guide.display())))
}

fn run() -> Result<(), Box<dyn Error>> {
    let event: Value = serde_json::from_reader(io::stdin().lock())?;
    if !should_activate(&event) {
        return Ok(());
    }
    let output = json!({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": load_policy()?
        }
    });
    serde_json::to_writer(io::stdout().lock(), &output)?;
    io::stdout().write_all(b"\n")?;
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("Solute hook skipped: {error}");
    }
}

#[cfg(test)]
mod tests {
    use super::{is_sol_model, opted_out};

    #[test]
    fn model_gate_accepts_only_sol_slugs() {
        for model in ["sol", "gpt-5.6-sol", "gpt-5.7-sol", "vendor-sol-preview"] {
            assert!(is_sol_model(model), "{model}");
        }
        for model in ["", "gpt-5.6-terra", "gpt-5.6-luna", "gpt-5.5"] {
            assert!(!is_sol_model(model), "{model}");
        }
    }

    #[test]
    fn opt_out_forms_are_case_insensitive() {
        for prompt in [
            "Don't use /solute for this one",
            "DO NOT USE SOLUTE",
            "Please don't use $solute today",
        ] {
            assert!(opted_out(prompt), "{prompt}");
        }
        assert!(!opted_out("Use Solute"));
    }
}
