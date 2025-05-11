import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Model configuration
model_name = "gpt2"
# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    
    # Get parameters with defaults
    prompt = data.get('prompt', "What is the name of the capital city of Pakistan?")
    max_length = data.get('max_length', 50)
    
    # Validate max_length
    if max_length <= 0:
        return jsonify({"error": "max_length must be greater than 0"}), 400
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs.input_ids,
            attention_mask=inputs.get('attention_mask', None),
            max_length=max_length
        )
    
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    response = text.split("\n\n")
    
    return jsonify({
        "generated_text": response
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
