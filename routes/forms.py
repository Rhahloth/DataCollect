from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import (AgronomicRecord, 
                    DiseaseRecord, 
                    FieldConditionRecord, 
                    GreenhouseConditionRecord,
                   GrowthFieldRecord, 
                   GrowthGreenhouseRecord, 
                   YieldFieldRecord, 
                   YieldGreenhouseRecord)
from db import db
from sheets_utils import sync_to_sheets

from datetime import datetime

import pandas as pd
from flask import send_file
from io import BytesIO

bp = Blueprint("forms", __name__, url_prefix="/form")

SHEET_MAP = {
    "AgronomicRecord": "Agronomic",
    "DiseaseRecord": "Disease",
    "FieldConditionRecord": "Field Condition",
    "GreenhouseConditionRecord": "Greenhouse Condition",
    "GrowthFieldRecord": "Growth (Field)",
    "GrowthGreenhouseRecord": "Growth (Greenhouse)",
    "YieldFieldRecord": "Yield (Field)",
    "YieldGreenhouseRecord": "Yield (Greenhouse)",
}

def save_and_sync(record):
    """Save record locally, try to sync to Google Sheets, and update status."""
    db.session.add(record)
    db.session.commit() 

    sheet_name = SHEET_MAP[record.__class__.__name__]
    if sync_to_sheets(record, sheet_name):
        record.synced = True
        db.session.commit()
        return True
    return False

def generate_dropdown_list(prefix: str, count: int):
    """Generate dropdown options like 'Genotype 1'...'Genotype 90'."""
    return [f"{prefix} {i}" for i in range(1, count + 1)]

@bp.route("/agronomic", methods=["GET", "POST"])
def agronomic():
    # Step 1: Generate dropdown lists
    crops = generate_dropdown_list("Crop", 5)
    blocks = generate_dropdown_list("Block", 90)
    genotypes = generate_dropdown_list("Genotype", 90)
    replications = generate_dropdown_list("Replication", 3)

    if request.method == "POST":
        try:
            # Step 2: Create record from form data
            record = AgronomicRecord(
                crop=request.form.get("crop"),
                block=request.form.get("block"),
                replication=request.form.get("replication"),
                plot_number=request.form.get("plot_number"),
                genotype=request.form.get("genotype"),
                days_heading=int(request.form.get("days_heading")) if request.form.get("days_heading") else None,
                days_maturity=int(request.form.get("days_maturity")) if request.form.get("days_maturity") else None,
                plant_height=float(request.form.get("plant_height")) if request.form.get("plant_height") else None,
                tillers=int(request.form.get("tillers")) if request.form.get("tillers") else None,
                panicle_length=float(request.form.get("panicle_length")) if request.form.get("panicle_length") else None,
                grain_yield=float(request.form.get("grain_yield")) if request.form.get("grain_yield") else None,
                grain_weight=float(request.form.get("grain_weight")) if request.form.get("grain_weight") else None,
                spikelets_total=int(request.form.get("spikelets_total")) if request.form.get("spikelets_total") else None,
                spikelets_filled=int(request.form.get("spikelets_filled")) if request.form.get("spikelets_filled") else None,
                fertility=float(request.form.get("fertility")) if request.form.get("fertility") else None,
                observation_date=datetime.strptime(request.form.get("observation_date"), "%Y-%m-%d").date()
                    if request.form.get("observation_date") else None,
                observer=request.form.get("observer"),
                remarks=request.form.get("remarks"),
            )

            # Step 3: Save to database
            db.session.add(record)
            db.session.commit()

            # Step 4: Sync with Google Sheets
            if save_and_sync(record):
                flash("Data saved & synced!", "success")
            else:
                flash("Data saved (pending sync)", "warning")

        except Exception as e:
            # Step 5: Handle errors
            db.session.rollback()
            flash(f"Error saving data: {e}", "danger")

        # Step 6: Redirect
        return redirect(url_for("main.dashboard"))

    # Step 7: Render template with dropdown data
    return render_template(
        "forms/agronomic.html",
        crops=crops,
        blocks=blocks,
        genotypes=genotypes,
        replications=replications
    )

# --- Disease Form ---
@bp.route("/disease", methods=["GET", "POST"])
def disease():
    # Step 1: Generate dropdown lists
    crops = generate_dropdown_list("Crop", 5)
    blocks = generate_dropdown_list("Block", 90)
    genotypes = generate_dropdown_list("Genotype", 90)
    replications = generate_dropdown_list("Replication", 3)

    if request.method == "POST":
        try:
            # Step 2: Create record from form data
            record = DiseaseRecord(
                crop=request.form.get("crop"),
                block=request.form.get("block"),
                genotype=request.form.get("genotype"),
                replication=request.form.get("replication"),
                plot_number=request.form.get("plot_number"),
                panicles_t1=int(request.form.get("panicles_t1")) if request.form.get("panicles_t1") else None,
                infected_t1=int(request.form.get("infected_t1")) if request.form.get("infected_t1") else None,
                incidence_t1=float(request.form.get("incidence_t1")) if request.form.get("incidence_t1") else None,
                panicles_t2=int(request.form.get("panicles_t2")) if request.form.get("panicles_t2") else None,
                infected_t2=int(request.form.get("infected_t2")) if request.form.get("infected_t2") else None,
                incidence_t2=float(request.form.get("incidence_t2")) if request.form.get("incidence_t2") else None,
                panicles_t3=int(request.form.get("panicles_t3")) if request.form.get("panicles_t3") else None,
                infected_t3=int(request.form.get("infected_t3")) if request.form.get("infected_t3") else None,
                incidence_t3=float(request.form.get("incidence_t3")) if request.form.get("incidence_t3") else None,
                severity_t1=int(request.form.get("severity_t1")) if request.form.get("severity_t1") else None,
                severity_t2=int(request.form.get("severity_t2")) if request.form.get("severity_t2") else None,
                severity_t3=int(request.form.get("severity_t3")) if request.form.get("severity_t3") else None,
                days_first_symptom=int(request.form.get("days_first_symptom")) if request.form.get("days_first_symptom") else None,
                notes=request.form.get("notes"),
            )

            # Step 3: Save to database
            db.session.add(record)
            db.session.commit()

            # Step 4: Sync with Google Sheets
            if save_and_sync(record):
                flash("Data saved & synced!", "success")
            else:
                flash("Data saved (pending sync)", "warning")

            # Step 5: Confirmation and redirect
            flash("Disease data saved!", "success")
            return redirect(url_for("main.dashboard"))

        except Exception as e:
            # Step 6: Handle errors
            db.session.rollback()
            flash(f"Error saving disease record: {e}", "danger")

    # Step 7: Render template with dropdown data
    return render_template(
        "forms/disease.html",
        crops=crops,
        blocks=blocks,
        genotypes=genotypes,
        replications=replications
    )

@bp.route("/field", methods=["GET", "POST"])
def field_condition():
    # Step 1: Generate dropdown lists
    crops = generate_dropdown_list("Crop", 5)
    blocks = generate_dropdown_list("Block", 90)
    genotypes = generate_dropdown_list("Genotype", 90)
    replications = generate_dropdown_list("Replication", 3)

    if request.method == "POST":
        try:
            # Step 2: Create record from form data
            record = FieldConditionRecord(
                crop=request.form.get("crop"),
                block=request.form.get("block"),
                genotype=request.form.get("genotype"),
                replication=request.form.get("replication"),
                date=datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
                     if request.form.get("date") else None,
                location=request.form.get("location"),
                soil_type=request.form.get("soil_type"),
                fertility_status=request.form.get("fertility_status"),
                temp_min=float(request.form.get("temp_min")) if request.form.get("temp_min") else None,
                temp_max=float(request.form.get("temp_max")) if request.form.get("temp_max") else None,
                temp_avg=float(request.form.get("temp_avg")) if request.form.get("temp_avg") else None,
                humidity=float(request.form.get("humidity")) if request.form.get("humidity") else None,
                rainfall=float(request.form.get("rainfall")) if request.form.get("rainfall") else None,
                notes=request.form.get("notes"),
            )

            # Step 3: Save to database
            db.session.add(record)
            db.session.commit()

            # Step 4: Sync to Google Sheets
            if save_and_sync(record):
                flash("Data saved & synced!", "success")
            else:
                flash("Data saved (pending sync)", "warning")

            # Step 5: Confirm and redirect
            flash("Field condition data saved!", "success")
            return redirect(url_for("main.dashboard"))

        except Exception as e:
            # Step 6: Handle errors
            db.session.rollback()
            flash(f"Error saving field condition: {e}", "danger")

    # Step 7: Render template with dropdown data
    return render_template(
        "forms/field_condition.html",
        crops=crops,
        blocks=blocks,
        genotypes=genotypes,
        replications=replications
    )

# --- Greenhouse Condition Form ---
@bp.route("/greenhouse", methods=["GET", "POST"])
def greenhouse_condition():
    # Step 1: Generate dropdown lists
    crops = generate_dropdown_list("Crop", 5)
    genotypes = generate_dropdown_list("Genotype", 90)
    replications = generate_dropdown_list("Replication", 3)

    if request.method == "POST":
        try:
            # Step 2: Create record from form data
            record = GreenhouseConditionRecord(
                crop=request.form.get("crop"),
                genotype=request.form.get("genotype"),
                replication=request.form.get("replication"),
                date=datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
                     if request.form.get("date") else None,
                location=request.form.get("location"),
                temp_min=float(request.form.get("temp_min")) if request.form.get("temp_min") else None,
                temp_max=float(request.form.get("temp_max")) if request.form.get("temp_max") else None,
                temp_avg=float(request.form.get("temp_avg")) if request.form.get("temp_avg") else None,
                humidity=float(request.form.get("humidity")) if request.form.get("humidity") else None,
                light_intensity=request.form.get("light_intensity"),
                inoculum=request.form.get("inoculum"),
                spray_timing=request.form.get("spray_timing"),
                spray_frequency=int(request.form.get("spray_frequency")) if request.form.get("spray_frequency") else None,
                notes=request.form.get("notes"),
            )

            # Step 3: Save to database
            db.session.add(record)
            db.session.commit()

            # Step 4: Sync to Google Sheets
            if save_and_sync(record):
                flash("Data saved & synced!", "success")
            else:
                flash("Data saved (pending sync)", "warning")

            # Step 5: Confirm and redirect
            flash("Greenhouse condition data saved!", "success")
            return redirect(url_for("main.dashboard"))

        except Exception as e:
            # Step 6: Handle errors
            db.session.rollback()
            flash(f"Error saving greenhouse condition: {e}", "danger")

    # Step 7: Render template with dropdown data
    return render_template(
        "forms/greenhouse_condition.html",
        crops=crops,
        genotypes=genotypes,
        replications=replications
    )

# --- Growth (Field) Form ---
@bp.route("/growth_field", methods=["GET", "POST"])
def growth_field():
    # Step 1: Generate dropdown lists
    crops = generate_dropdown_list("Crop", 5)
    blocks = generate_dropdown_list("Block", 90)
    genotypes = generate_dropdown_list("Genotype", 90)
    replications = generate_dropdown_list("Replication", 3)

    if request.method == "POST":
        try:
            # Step 2: Create record from form data
            record = GrowthFieldRecord(
                crop=request.form.get("crop"),
                block=request.form.get("block"),
                genotype=request.form.get("genotype"),
                replication=request.form.get("replication"),
                plot_number=request.form.get("plot_number"),
                days_flowering=int(request.form.get("days_flowering")) if request.form.get("days_flowering") else None,
                days_maturity=int(request.form.get("days_maturity")) if request.form.get("days_maturity") else None,
                plant_height=float(request.form.get("plant_height")) if request.form.get("plant_height") else None,
                tillers=int(request.form.get("tillers")) if request.form.get("tillers") else None,
                notes=request.form.get("notes"),
            )

            # Step 3: Save to database
            db.session.add(record)
            db.session.commit()

            # Step 4: Sync to Google Sheets
            if save_and_sync(record):
                flash("Data saved & synced!", "success")
            else:
                flash("Data saved (pending sync)", "warning")

            # Step 5: Confirm and redirect
            flash("Growth (Field) data saved!", "success")
            return redirect(url_for("main.dashboard"))

        except Exception as e:
            # Step 6: Handle errors
            db.session.rollback()
            flash(f"Error saving Growth (Field) record: {e}", "danger")

    # Step 7: Render template with dropdown data
    return render_template(
        "forms/growth_field.html",
        crops=crops,
        blocks=blocks,
        genotypes=genotypes,
        replications=replications
    )

# --- Growth (Greenhouse) Form ---
@bp.route("/growth_greenhouse", methods=["GET", "POST"])
def growth_greenhouse():
    # Step 1: Generate dropdown lists
    crops = generate_dropdown_list("Crop", 5)
    genotypes = generate_dropdown_list("Genotype", 90)
    replications = generate_dropdown_list("Replication", 3)

    if request.method == "POST":
        try:
            # Step 2: Create record from form data
            record = GrowthGreenhouseRecord(
                crop=request.form.get("crop"),
                genotype=request.form.get("genotype"),
                replication=request.form.get("replication"),
                greenhouse_id=request.form.get("greenhouse_id"),
                days_flowering=int(request.form.get("days_flowering")) if request.form.get("days_flowering") else None,
                days_maturity=int(request.form.get("days_maturity")) if request.form.get("days_maturity") else None,
                plant_height=float(request.form.get("plant_height")) if request.form.get("plant_height") else None,
                tillers=int(request.form.get("tillers")) if request.form.get("tillers") else None,
                notes=request.form.get("notes"),
            )

            # Step 3: Save to database
            db.session.add(record)
            db.session.commit()

            # Step 4: Sync to Google Sheets
            if save_and_sync(record):
                flash("Data saved & synced!", "success")
            else:
                flash("Data saved (pending sync)", "warning")

            # Step 5: Confirm and redirect
            flash("Growth (Greenhouse) data saved!", "success")
            return redirect(url_for("main.dashboard"))

        except Exception as e:
            # Step 6: Handle errors
            db.session.rollback()
            flash(f"Error saving Growth (Greenhouse) record: {e}", "danger")

    # Step 7: Render template with dropdown data
    return render_template(
        "forms/growth_greenhouse.html",
        crops=crops,
        genotypes=genotypes,
        replications=replications
    )

# --- Yield (Field) Form ---
@bp.route("/yield_field", methods=["GET", "POST"])
def yield_field():
    # Step 1: Generate dropdown lists
    crops = generate_dropdown_list("Crop", 5)
    blocks = generate_dropdown_list("Block", 90)
    genotypes = generate_dropdown_list("Genotype", 90)
    replications = generate_dropdown_list("Replication", 3)

    if request.method == "POST":
        try:
            # Step 2: Create record from form data
            record = YieldFieldRecord(
                crop=request.form.get("crop"),
                block=request.form.get("block"),
                genotype=request.form.get("genotype"),
                replication=request.form.get("replication"),
                plot_number=request.form.get("plot_number"),
                panicles=int(request.form.get("panicles")) if request.form.get("panicles") else None,
                panicle_length=float(request.form.get("panicle_length")) if request.form.get("panicle_length") else None,
                filled_grains=int(request.form.get("filled_grains")) if request.form.get("filled_grains") else None,
                unfilled_grains=int(request.form.get("unfilled_grains")) if request.form.get("unfilled_grains") else None,
                grain_weight=float(request.form.get("grain_weight")) if request.form.get("grain_weight") else None,
                yield_plant=float(request.form.get("yield_plant")) if request.form.get("yield_plant") else None,
                yield_plot=float(request.form.get("yield_plot")) if request.form.get("yield_plot") else None,
                notes=request.form.get("notes"),
            )

            # Step 3: Save to database
            db.session.add(record)
            db.session.commit()

            # Step 4: Sync to Google Sheets
            if save_and_sync(record):
                flash("Data saved & synced!", "success")
            else:
                flash("Data saved (pending sync)", "warning")

            # Step 5: Confirm and redirect
            flash("Yield (Field) data saved!", "success")
            return redirect(url_for("main.dashboard"))

        except Exception as e:
            # Step 6: Handle errors
            db.session.rollback()
            flash(f"Error saving Yield (Field) record: {e}", "danger")

    # Step 7: Render template with dropdown data
    return render_template(
        "forms/yield_field.html",
        crops=crops,
        blocks=blocks,
        genotypes=genotypes,
        replications=replications
    )

# --- Yield (Greenhouse) Form ---
@bp.route("/yield_greenhouse", methods=["GET", "POST"])
def yield_greenhouse():
    # Step 1: Generate dropdown lists
    crops = generate_dropdown_list("Crop", 5)
    genotypes = generate_dropdown_list("Genotype", 90)
    replications = generate_dropdown_list("Replication", 3)

    if request.method == "POST":
        try:
            # Step 2: Create record from form data
            record = YieldGreenhouseRecord(
                crop=request.form.get("crop"),
                genotype=request.form.get("genotype"),
                replication=request.form.get("replication"),
                greenhouse_id=request.form.get("greenhouse_id"),
                panicles=int(request.form.get("panicles")) if request.form.get("panicles") else None,
                panicle_length=float(request.form.get("panicle_length")) if request.form.get("panicle_length") else None,
                filled_grains=int(request.form.get("filled_grains")) if request.form.get("filled_grains") else None,
                unfilled_grains=int(request.form.get("unfilled_grains")) if request.form.get("unfilled_grains") else None,
                grain_weight=float(request.form.get("grain_weight")) if request.form.get("grain_weight") else None,
                yield_plant=float(request.form.get("yield_plant")) if request.form.get("yield_plant") else None,
                yield_tray=float(request.form.get("yield_tray")) if request.form.get("yield_tray") else None,
                notes=request.form.get("notes"),
            )

            # Step 3: Save to database
            db.session.add(record)
            db.session.commit()

            # Step 4: Sync to Google Sheets
            if save_and_sync(record):
                flash("Data saved & synced!", "success")
            else:
                flash("Data saved (pending sync)", "warning")

            # Step 5: Confirm and redirect
            flash("Yield (Greenhouse) data saved!", "success")
            return redirect(url_for("main.dashboard"))

        except Exception as e:
            # Step 6: Handle errors
            db.session.rollback()
            flash(f"Error saving Yield (Greenhouse) record: {e}", "danger")

    # Step 7: Render template with dropdown data
    return render_template(
        "forms/yield_greenhouse.html",
        crops=crops,
        genotypes=genotypes,
        replications=replications
    )

@bp.route("/sync_all", methods=["POST"])
def sync_all():
    try:
        models = [
            (AgronomicRecord, "Agronomic"),
            (DiseaseRecord, "Disease"),
            (FieldConditionRecord, "Field Condition"),
            (GreenhouseConditionRecord, "Greenhouse Condition"),
            (GrowthFieldRecord, "Growth (Field)"),
            (GrowthGreenhouseRecord, "Growth (Greenhouse)"),
            (YieldFieldRecord, "Yield (Field)"),
            (YieldGreenhouseRecord, "Yield (Greenhouse)"),
        ]

        results = {}
        total_synced = 0

        for model, sheet in models:
            unsynced = db.session.query(model).filter_by(synced=False).all()
            print(f"Checking {sheet} → found {len(unsynced)} unsynced rows")

            synced_here = 0
            for row in unsynced:
                print(f"  → Attempting to sync {sheet} row id={row.id}")
                result = sync_to_sheets(row, sheet)

                if result in [True, "already"]:
                    row.synced = True
                    synced_here += 1
                    if result == "already":
                        print(f"    Already in sheet, marking synced row id={row.id}")
                    else:
                        print(f"    Synced row id={row.id}")
                else:
                    print(f"    Failed to sync row id={row.id}")

            if synced_here > 0:
                db.session.commit()  # commit after each model batch
                results[sheet] = synced_here
                total_synced += synced_here
                print(f"Finished {sheet}, synced {synced_here} rows")

        db.session.commit()  # final safeguard
        print(f"Total synced across all models: {total_synced}")
        print(f"Breakdown: {results}")

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({
                "message": f"{total_synced} records synced",
                "details": results
            })
        else:
            flash(f"{total_synced} records synced", "success")
            return redirect(url_for("main.dashboard"))

    except Exception as e:
        db.session.rollback()
        print(f"Error in sync_all: {e}")
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": str(e)}), 500
        else:
            flash(f"Error syncing records: {e}", "danger")
            return redirect(url_for("main.dashboard"))

@bp.route("/download/all")
def download_all():
    try:
        output = BytesIO()

        forms = [
            (AgronomicRecord, "Agronomic"),
            (DiseaseRecord, "Disease"),
            (FieldConditionRecord, "Field Condition"),
            (GreenhouseConditionRecord, "Greenhouse Condition"),
            (GrowthFieldRecord, "Growth (Field)"),
            (GrowthGreenhouseRecord, "Growth (Greenhouse)"),
            (YieldFieldRecord, "Yield (Field)"),
            (YieldGreenhouseRecord, "Yield (Greenhouse)"),
        ]

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            for model, sheet_name in forms:
                records = model.query.all()
                if records:
                    df = pd.DataFrame([r.__dict__ for r in records])
                    if "_sa_instance_state" in df.columns:
                        df = df.drop(columns=["_sa_instance_state"])
                else:
                    df = pd.DataFrame(columns=["No Data"])
                df.to_excel(writer, index=False, sheet_name=sheet_name)

        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="DataCollect_All.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        return f"Error exporting Excel: {e}", 500
