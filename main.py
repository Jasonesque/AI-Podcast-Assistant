import os
import argparse
from core.downloader import download_audio
from core.asr_engine import transcribe_audio
from core.llm_agent import summarize_transcript
from core.file_manager import save_to_obsidian

def process_podcast(url: str):
    print("=== Podcast AI Assistant Pipeline Started ===")
    audio_path = None
    
    try:
        # 1. Download
        print(f"\n[1/4] Downloading audio from {url}...")
        audio_path, title = download_audio(url)
        
        # 2. Transcribe
        print(f"\n[2/4] Transcribing audio...")
        transcript = transcribe_audio(audio_path)
        
        # 3. Summarize
        print(f"\n[3/4] Summarizing with MIMO API...")
        summary = summarize_transcript(transcript, title)
        
        # 4. Save
        print(f"\n[4/4] Saving to Knowledge Base...")
        save_to_obsidian(title, summary, transcript)
        
        print("\n=== Pipeline Completed Successfully! ===")
        return summary

    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {str(e)}")
        raise e

    finally:
        # Clean up temp audio no matter what (success or crash)
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                print(f"Cleaned up temporary audio: {audio_path}")
            except Exception as cleanup_error:
                print(f"Failed to clean up {audio_path}: {cleanup_error}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Podcast AI Feishu Bot - Local Tester")
    parser.add_argument("url", type=str, help="The URL of the podcast/video to process")
    args = parser.parse_args()
    
    process_podcast(args.url)
