yt-dlp.exe -f ba "https://www.youtube.com/watch?v=psc9qq4Jg5Y" -P I:/gdg -x --audio-format mp3
yt-dlp.exe -f ba "https://www.youtube.com/watch?v=UoAVE12aWOk" -P I:/music -x --audio-format flac
yt-dlp.exe https://www.youtube.com/watch?v=dtxlmaiKByQ --remux-video webm>mkv
ffmpeg -i input.webm -vn audio_only.mp3
ffmpeg -i movie.webm movie.mp4