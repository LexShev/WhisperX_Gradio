# WhisperX Web Interface for Broadcast Subtitles


## Overview

This project adapts [WhisperX](https://github.com/m-bain/whisperX) into an easy-to-use web interface for our broadcasting company's needs. It enables automated subtitle generation for video content to comply with accessibility regulations for hearing-impaired viewers.

**Key Features:**
- 🚀 Batch processing of multiple video files
- 🌐 User-friendly Gradio web interface
- 🎬 Automatic speech recognition and subtitle generation
- ⏱️ Faster processing than original Whisper implementation
- 📝 Output in standard subtitle formats (SRT, VTT)

## Why This Matters

We're legally required to provide accessible content for hearing-impaired audiences. This solution:
- Ensures compliance with broadcasting regulations
- Saves hundreds of manual work hours
- Maintains consistent quality across all programs

## Technical Adaptations

**Our version includes:**
- Custom preprocessing for broadcast audio quality
- Optimized model parameters for our content types
- Automatic speaker identification for multi-voice programs
- Integration with our media asset management system

## License

This project is built upon WhisperX (MIT License) and contains proprietary adaptations for internal company use only.