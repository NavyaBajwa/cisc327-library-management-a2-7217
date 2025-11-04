from flask import Blueprint, render_template, request, flash
from services.library_service import get_patron_status_report

report_bp = Blueprint('report', __name__)

@report_bp.route('/report')
def patron_report():

    patron_id = request.args.get('patron_id', '').strip()
    report = None

    if patron_id:
        if not patron_id.isdigit() or len(patron_id) != 6:
            flash("Invalid Patron ID. Must be exactly 6 digits.", "error")
        else:
            report = get_patron_status_report(patron_id)
            if not report:
                flash('No report found for this Patron ID.', 'error')

    
    return render_template('report.html', patron_id=patron_id, report=report)