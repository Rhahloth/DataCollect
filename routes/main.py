from flask import Blueprint, render_template
from models import (AgronomicRecord, 
                    DiseaseRecord, 
                    FieldConditionRecord, 
                    GreenhouseConditionRecord,
                   GrowthFieldRecord, 
                   GrowthGreenhouseRecord, 
                   YieldFieldRecord, 
                   YieldGreenhouseRecord)
from app import db

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("/")
def home():
    # Renders base.html directly from /templates
    return render_template("home.html")

@bp.route("/offline")
def offline():
    return render_template("offline.html")


@bp.route("/dashboard")
def dashboard():
    # --- Counts per table ---
    agronomic_count = db.session.query(AgronomicRecord).count()
    disease_count = db.session.query(DiseaseRecord).count()
    field_count = db.session.query(FieldConditionRecord).count()
    greenhouse_count = db.session.query(GreenhouseConditionRecord).count()
    growth_field_count = db.session.query(GrowthFieldRecord).count()
    growth_greenhouse_count = db.session.query(GrowthGreenhouseRecord).count()
    yield_field_count = db.session.query(YieldFieldRecord).count()
    yield_greenhouse_count = db.session.query(YieldGreenhouseRecord).count()

    total_records = (
        agronomic_count + disease_count + field_count +
        greenhouse_count + growth_field_count +
        growth_greenhouse_count + yield_field_count +
        yield_greenhouse_count
    )

    unsynced_counts = {
        "Agronomic": db.session.query(AgronomicRecord).filter_by(synced=False).count(),
        "Disease": db.session.query(DiseaseRecord).filter_by(synced=False).count(),
        "Field Condition": db.session.query(FieldConditionRecord).filter_by(synced=False).count(),
        "Greenhouse Condition": db.session.query(GreenhouseConditionRecord).filter_by(synced=False).count(),
        "Growth (Field)": db.session.query(GrowthFieldRecord).filter_by(synced=False).count(),
        "Growth (Greenhouse)": db.session.query(GrowthGreenhouseRecord).filter_by(synced=False).count(),
        "Yield (Field)": db.session.query(YieldFieldRecord).filter_by(synced=False).count(),
        "Yield (Greenhouse)": db.session.query(YieldGreenhouseRecord).filter_by(synced=False).count(),
    }


    # --- Latest entry timestamp ---
    last_entry_times = []
    for model in [
        AgronomicRecord, DiseaseRecord, FieldConditionRecord,
        GreenhouseConditionRecord, GrowthFieldRecord,
        GrowthGreenhouseRecord, YieldFieldRecord, YieldGreenhouseRecord
    ]:
        result = db.session.query(model.created_at).order_by(model.created_at.desc()).first()
        if result:
            last_entry_times.append(result[0])
    last_entry = max(last_entry_times).strftime("%Y-%m-%d %H:%M") if last_entry_times else None

    # --- Recent entries (normalized for template) ---
    recent_entries = []

    def add_entries(model, form_type, identifier_field=None, observer_field=None):
        rows = db.session.query(model).order_by(model.created_at.desc()).limit(3).all()
        for row in rows:
            identifier = getattr(row, identifier_field, None) if identifier_field else "-"
            observer = getattr(row, observer_field, None) if observer_field else "-"
            recent_entries.append({
                "form_type": form_type,
                "identifier": identifier or "—",
                "observer": observer or "—",
                "date": row.created_at.strftime("%Y-%m-%d %H:%M")
            })

    # Map each model to a label + fields
    add_entries(AgronomicRecord, "Agronomic", "plot_number", "observer")
    add_entries(DiseaseRecord, "Disease", "plot_number")
    add_entries(FieldConditionRecord, "Field Condition", "location")
    add_entries(GreenhouseConditionRecord, "Greenhouse Condition", "location")
    add_entries(GrowthFieldRecord, "Growth (Field)", "plot_number")
    add_entries(GrowthGreenhouseRecord, "Growth (Greenhouse)", "greenhouse_id")
    add_entries(YieldFieldRecord, "Yield (Field)", "plot_number")
    add_entries(YieldGreenhouseRecord, "Yield (Greenhouse)", "greenhouse_id")

    # sort across all models and take top 5
    recent_entries = sorted(recent_entries, key=lambda x: x["date"], reverse=True)[:5]

    return render_template(
        "dashboard.html",
        total_genotypes=agronomic_count,
        total_records=total_records,
        last_entry=last_entry,
        recent_entries=recent_entries,
        # individual form counts
        agronomic_count=agronomic_count,
        disease_count=disease_count,
        field_count=field_count,
        greenhouse_count=greenhouse_count,
        growth_field_count=growth_field_count,
        growth_greenhouse_count=growth_greenhouse_count,
        yield_field_count=yield_field_count,
        yield_greenhouse_count=yield_greenhouse_count,
        unsynced_counts=unsynced_counts
    )
