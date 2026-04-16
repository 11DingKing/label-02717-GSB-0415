import os
import sys
import traceback
# 自动同意 Coqui TTS 许可协议（非商业用途）
os.environ["COQUI_TOS_AGREED"] = "1"

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from TTS.api import TTS
import uuid
import tempfile

app = Flask(__name__)
CORS(app)

# 初始化 TTS 模型（支持语音克隆的 YourTTS 模型）
print("Loading YourTTS model for voice cloning...", flush=True)
tts = TTS("tts_models/multilingual/multi-dataset/your_tts", progress_bar=False)
print("Model loaded successfully!", flush=True)

UPLOAD_FOLDER = tempfile.mkdtemp()
OUTPUT_FOLDER = tempfile.mkdtemp()

@app.route('/api/clone', methods=['POST'])
def clone_voice():
    print("Received clone request", flush=True)
    
    if 'audio' not in request.files:
        return jsonify({'error': '请上传音频文件'}), 400
    
    text = request.form.get('text', '')
    if not text:
        return jsonify({'error': '请输入文本内容'}), 400
    
    audio_file = request.files['audio']
    print(f"Audio file: {audio_file.filename}, Text: {text}", flush=True)
    
    # 保存上传的音频
    audio_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, f"{audio_id}.wav")
    output_path = os.path.join(OUTPUT_FOLDER, f"{audio_id}_output.wav")
    
    audio_file.save(input_path)
    print(f"Saved audio to: {input_path}", flush=True)
    
    try:
        # 检查文件是否存在且有内容
        file_size = os.path.getsize(input_path)
        print(f"Input file size: {file_size} bytes", flush=True)
        
        if file_size < 1000:
            return jsonify({'error': '音频文件太小，请上传有效的音频文件'}), 400
        
        print("Starting TTS synthesis...", flush=True)
        # 使用上传的音频作为参考进行语音克隆
        # 注意：YourTTS 模型仅支持英语(en)、葡萄牙语(pt-br)、法语(fr-fr)
        # 不支持中文，中文文本会被当作英文发音处理
        tts.tts_to_file(
            text=text,
            speaker_wav=input_path,
            language="en",
            file_path=output_path
        )
        print(f"TTS completed, output: {output_path}", flush=True)
        
        # 检查输出文件
        if not os.path.exists(output_path):
            return jsonify({'error': '语音生成失败，输出文件不存在'}), 500
        
        output_size = os.path.getsize(output_path)
        print(f"Output file size: {output_size} bytes", flush=True)
        
        # 读取文件内容后立即清理
        with open(output_path, 'rb') as f:
            audio_data = f.read()
        
        # 清理输出文件
        if os.path.exists(output_path):
            os.remove(output_path)
        
        from flask import Response
        return Response(
            audio_data,
            mimetype='audio/wav',
            headers={'Content-Disposition': 'attachment; filename=cloned_voice.wav'}
        )
    except Exception as e:
        error_msg = str(e)
        print(f"Error during TTS: {error_msg}", flush=True)
        traceback.print_exc()
        # 清理输出文件（如果存在）
        if os.path.exists(output_path):
            os.remove(output_path)
        return jsonify({'error': f'语音生成失败: {error_msg}'}), 500
    finally:
        # 清理上传的文件
        if os.path.exists(input_path):
            os.remove(input_path)

@app.route('/health', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'voice-cloning-backend'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
