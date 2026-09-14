use std::fs;
use tauri::Manager;

/// Returns the path of the progress file inside the app data folder.
fn progress_path(app: &tauri::AppHandle) -> Result<std::path::PathBuf, String> {
    let dir = app.path().app_data_dir().map_err(|e| e.to_string())?;
    fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
    Ok(dir.join("progress.json"))
}

#[tauri::command]
fn load_progress(app: tauri::AppHandle) -> Result<String, String> {
    let path = progress_path(&app)?;
    if !path.exists() {
        return Ok(String::from("{}"));
    }
    fs::read_to_string(path).map_err(|e| e.to_string())
}

#[tauri::command]
fn save_progress(app: tauri::AppHandle, data: String) -> Result<(), String> {
    let path = progress_path(&app)?;
    fs::write(path, data).map_err(|e| e.to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![load_progress, save_progress])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
