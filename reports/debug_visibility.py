from flask import Blueprint, jsonify, request
from .main_routes import parse_rpt_params_universal, build_dynamic_parameters
from database import get_db_connection

debug_visibility_bp = Blueprint('debug_visibility', __name__)

@debug_visibility_bp.route('/test-parameter-visibility/<report_id>')
def test_parameter_visibility(report_id):
    """Test parameter visibility filtering for a specific report"""
    
    try:
        # Get report configuration from database
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT RPT_PARAMS FROM RPT_REPORT_MASTER WHERE RPT_ID = :report_id", [report_id])
            result = cursor.fetchone()
            
            if not result:
                return jsonify({
                    'error': f'Report {report_id} not found',
                    'report_id': report_id
                }), 404
            
            rpt_params_clob = result[0]
            if hasattr(rpt_params_clob, 'read'):
                rpt_params_str = rpt_params_clob.read()
            else:
                rpt_params_str = str(rpt_params_clob)
            
            # Parse parameters using the universal parser
            filtered_params = parse_rpt_params_universal(rpt_params_str, 'SQL')
            
            response = {
                'report_id': report_id,
                'raw_config_length': len(rpt_params_str),
                'filtered_parameters_count': len(filtered_params),
                'filtered_parameters': [],
                'raw_config_preview': rpt_params_str[:500] + '...' if len(rpt_params_str) > 500 else rpt_params_str
            }
            
            for param in filtered_params:
                response['filtered_parameters'].append({
                    'name': param.get('name', 'Unknown'),
                    'field': param.get('field', 'N/A'),
                    'type': param.get('type', 'N/A'),
                    'visible': param.get('visible', True),
                    'required': param.get('required', False),
                    'default': param.get('default', '')
                })
            
            return jsonify(response)
        
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'report_id': report_id,
            'traceback': traceback.format_exc()
        }), 500

@debug_visibility_bp.route('/test-parameter-processing/<report_id>')
def test_parameter_processing(report_id):
    """Test parameter processing including hidden parameters"""
    
    try:
        # Get report configuration from database
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT RPT_ID, RPT_NAME, RPT_DESC, RPT_TYPE, RPT_PARAMS FROM RPT_REPORT_MASTER WHERE RPT_ID = :report_id", [report_id])
            result = cursor.fetchone()
            
            if not result:
                return jsonify({
                    'error': f'Report {report_id} not found',
                    'report_id': report_id
                }), 404
            
            rpt_id, rpt_name, rpt_desc, rpt_type, rpt_params_clob = result
            
            if hasattr(rpt_params_clob, 'read'):
                rpt_params_str = rpt_params_clob.read()
            else:
                rpt_params_str = str(rpt_params_clob)
            
            # Create report config like in main_routes.py
            import json
            rpt_params_dict = json.loads(rpt_params_str)
            
            report_config = {
                'id': rpt_id,
                'name': rpt_name,
                'description': rpt_desc,
                'type': rpt_type,
                'params': rpt_params_dict  # FIXED: use 'params' to match main code
            }
            
            # Simulate form data (only visible parameters)
            form_data = {
                'menu_id': 'T020101',
                'report_id': report_id,
                'reportType': 'detail',
                'to_dt': '31/12/2024',
                'fm_txn_code': '0', 
                'to_txn_code': 'ZZZZZZ',
                'outputFormat': 'view'
                # NOTE: FM_DT is missing - it should be added as hidden parameter
            }
            
            # Simulate session
            session = {
                'user_id': 'ADMIN',
                'comp_code': 'TTM'
            }
            
            # Call build_dynamic_parameters to test hidden parameter processing
            processed_params = build_dynamic_parameters(form_data, session, report_config)
            
            response = {
                'report_id': report_id,
                'original_form_data': form_data,
                'processed_parameters': processed_params,
                'parameters_config': rpt_params_dict.get('parameters', []),
                'hidden_parameter_test': 'fm_dt' in processed_params.get('params', processed_params)
            }
            
            return jsonify(response)
        
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'report_id': report_id,
            'traceback': traceback.format_exc()
        }), 500