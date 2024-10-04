from flask import Flask, render_template, request, jsonify
import grounded_llm  # Uncomment this when the LLM is ready

app = Flask(__name__)

# Category and dataflow data (sample data)
categories_data = {
    'IT Indicators': ['OECD.EDU.IMEP:DSD_EAG_IT@DF_EAG_IT_AGE(1.1)', 'OECD.EDU.IMEP:DSD_EAG_IT@DF_EAG_IT_ALL(1.1)'],
    'LSO Earnings and Employment': ['OECD.EDU.IMEP:DSD_EAG_LSO_EA@DF_LSO_EARN_DISTR_MEDIAN(1.0)', 'OECD.EDU.IMEP:DSD_EAG_LSO_EA@DF_LSO_EARN_REL_BEL(1.0)'],
    'UOE Financial': ['OECD.EDU.IMEP:DSD_EAG_UOE_FIN@DF_UOE_FIN_INDIC_SHARE_EDU_GOV(3.0)', 'OECD.EDU.IMEP:DSD_EAG_UOE_FIN@DF_UOE_FIN_INDIC_SOURCE_NATURE(3.0)'],
    'WT Indicators': ['OECD.EDU.IMEP:DSD_EAG_WT@DF_ACT_TCH(2.0)', 'OECD.EDU.IMEP:DSD_EAG_WT@DF_ALL(2.0)']
}

# Global bot instance (for demonstration purposes)
bot_instance = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_categories', methods=['GET'])
def get_categories():
    return jsonify(list(categories_data.keys()))

@app.route('/get_dataflows/<category>', methods=['GET'])
def get_dataflows(category):
    return jsonify(categories_data.get(category, []))

@app.route('/initialize_bot', methods=['POST'])
def initialize_bot():
    global bot_instance
    data = request.json
    dataflow = data.get('dataflow')

    # Simulate bot initialization
    bot_instance = grounded_llm.Bot(dataflow)  # Uncomment this when LLM is available
    #bot_instance = f"Initialized Bot with {dataflow}"  # Temporary message for testing

    return jsonify({'status': 'success', 'message': f'Bot initialized with dataflow: {dataflow}'})

@app.route('/chat', methods=['POST'])
def chat():
    global bot_instance
    data = request.json
    user_message = data['message']

    if not bot_instance:
        return jsonify({'response': "Bot is not initialized. Please select a category and dataflow, and click 'Initialize Bot'."})

    # Placeholder for bot's response
    # response = f"[Bot]: You said '{user_message}' (using dataflow: {bot_instance})"
    response = bot_instance.answer_question(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    print("Starting the app... on http://127.0.0.1:5000/")
    app.run(debug=True)
    