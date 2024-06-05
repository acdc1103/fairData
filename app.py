from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from metrics import access_points, uri_availbalility, license_availability, metadata_updated_last_month, category_availability, attribution_availability, description_analyzer, financial_standards_applicable, check_metadata, check_audience, identifier_accessible
from api_handler import retrieve_metadata, retrieve_data_sample
from utils import calculate_summary_grade
import logging

logging.basicConfig(level="INFO")

app = Flask(__name__)
CORS(app)


def run_all_metrics(uid):
    
    metadata = retrieve_metadata(uid)
    sample_data = retrieve_data_sample(uid)

    access_points_result = access_points(metadata)
    uri_availbalility_result = uri_availbalility(metadata)
    license_availability_result = license_availability(metadata)
    metadata_updated_last_month_result = metadata_updated_last_month(metadata)
    category_availability_result = category_availability(metadata)
    attribution_availability_result = attribution_availability(metadata)
    description_analyzer_result = description_analyzer(metadata)
    financial_standards_applicable_result = financial_standards_applicable(metadata, sample_data)
    check_audience_result = check_audience(metadata)
    identifier_accessible_result = identifier_accessible(metadata)
    check_metadata_result = check_metadata(metadata)
    
    return {
        'access_points': access_points_result,
        'uri_availability': uri_availbalility_result,
        'license_availability': license_availability_result,
        'metadata_updated_last_month': metadata_updated_last_month_result,
        'description_analyzer': description_analyzer_result,
        'category_availability': category_availability_result,
        'attribution_availability': attribution_availability_result,
        'financial_standards_applicable': financial_standards_applicable_result,
        'check_audience': check_audience_result,
        'identifier_accessible': identifier_accessible_result,
        'check_metadata': check_metadata_result
    }

    
@app.route('/run_metrics', methods=['POST'])
def run_metrics():
    data = request.json
    uid = data.get('uid')

    if not uid:
        return jsonify({'error': 'No URL provided'}), 400

    metrics_results = run_all_metrics(uid)
    summarized_grading = calculate_summary_grade(metrics_results)
    metrics_results['summary'] = summarized_grading
    return jsonify(metrics_results)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)