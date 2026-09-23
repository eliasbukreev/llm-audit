// Prevents console window on macOS when running in development mode
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    // Start the Tauri runtime with the backend server
    // Backend is expected to be running on localhost:8000
    tauri::Builder::default().run(tauri::generate_context!()).expect("error while running tauri application");
}
