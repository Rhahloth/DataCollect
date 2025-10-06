from db import db
from datetime import datetime
from zoneinfo import ZoneInfo

def Kampala_time():
    return datetime.now(ZoneInfo("Africa/Kampala"))

# --- 1. Agronomic & Morphological ---
class AgronomicRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50))              # Added
    block = db.Column(db.String(20))             # Added
    replication = db.Column(db.String(20))       # Added
    plot_number = db.Column(db.String(50))
    genotype = db.Column(db.String(100))
    days_heading = db.Column(db.Integer)
    days_maturity = db.Column(db.Integer)
    plant_height = db.Column(db.Float)
    tillers = db.Column(db.Integer)
    panicle_length = db.Column(db.Float)
    grain_yield = db.Column(db.Float)
    grain_weight = db.Column(db.Float)
    spikelets_total = db.Column(db.Integer)
    spikelets_filled = db.Column(db.Integer)
    fertility = db.Column(db.Float)
    observation_date = db.Column(db.Date)
    observer = db.Column(db.String(100))
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=Kampala_time)
    synced = db.Column(db.Boolean, default=False, nullable=False)


# --- 2. Disease ---
class DiseaseRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50))              # Added
    block = db.Column(db.String(20))             # Added
    genotype = db.Column(db.String(100))
    replication = db.Column(db.String(20))
    plot_number = db.Column(db.String(50))
    panicles_t1 = db.Column(db.Integer)
    infected_t1 = db.Column(db.Integer)
    incidence_t1 = db.Column(db.Float)
    panicles_t2 = db.Column(db.Integer)
    infected_t2 = db.Column(db.Integer)
    incidence_t2 = db.Column(db.Float)
    panicles_t3 = db.Column(db.Integer)
    infected_t3 = db.Column(db.Integer)
    incidence_t3 = db.Column(db.Float)
    severity_t1 = db.Column(db.Integer)
    severity_t2 = db.Column(db.Integer)
    severity_t3 = db.Column(db.Integer)
    days_first_symptom = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=Kampala_time)
    synced = db.Column(db.Boolean, default=False, nullable=False)


# --- 3. Field Condition ---
class FieldConditionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50))              # Added
    block = db.Column(db.String(20))             # Added
    genotype = db.Column(db.String(100))         # Added
    replication = db.Column(db.String(20))       # Added
    date = db.Column(db.Date)
    location = db.Column(db.String(100))
    soil_type = db.Column(db.String(50))
    fertility_status = db.Column(db.String(20))
    temp_min = db.Column(db.Float)
    temp_max = db.Column(db.Float)
    temp_avg = db.Column(db.Float)
    humidity = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=Kampala_time)
    synced = db.Column(db.Boolean, default=False, nullable=False)


# --- 4. Greenhouse Condition ---
class GreenhouseConditionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50))              # Added
    genotype = db.Column(db.String(100))         # Added
    replication = db.Column(db.String(20))       # Added
    date = db.Column(db.Date)
    location = db.Column(db.String(100))
    temp_min = db.Column(db.Float)
    temp_max = db.Column(db.Float)
    temp_avg = db.Column(db.Float)
    humidity = db.Column(db.Float)
    light_intensity = db.Column(db.String(50))
    inoculum = db.Column(db.String(50))
    spray_timing = db.Column(db.String(20))
    spray_frequency = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=Kampala_time)
    synced = db.Column(db.Boolean, default=False, nullable=False)


# --- 5. Growth (Field) ---
class GrowthFieldRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50))              # Added
    block = db.Column(db.String(20))             # Added
    genotype = db.Column(db.String(100))
    replication = db.Column(db.String(20))
    plot_number = db.Column(db.String(50))
    days_flowering = db.Column(db.Integer)
    days_maturity = db.Column(db.Integer)
    plant_height = db.Column(db.Float)
    tillers = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=Kampala_time)
    synced = db.Column(db.Boolean, default=False, nullable=False)


# --- 6. Growth (Greenhouse) ---
class GrowthGreenhouseRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50))              # Added
    genotype = db.Column(db.String(100))
    replication = db.Column(db.String(20))
    greenhouse_id = db.Column(db.String(50))
    days_flowering = db.Column(db.Integer)
    days_maturity = db.Column(db.Integer)
    plant_height = db.Column(db.Float)
    tillers = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=Kampala_time)
    synced = db.Column(db.Boolean, default=False, nullable=False)


# --- 7. Yield (Field) ---
class YieldFieldRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50))              # Added
    block = db.Column(db.String(20))             # Added
    genotype = db.Column(db.String(100))
    replication = db.Column(db.String(20))
    plot_number = db.Column(db.String(50))
    panicles = db.Column(db.Integer)
    panicle_length = db.Column(db.Float)
    filled_grains = db.Column(db.Integer)
    unfilled_grains = db.Column(db.Integer)
    grain_weight = db.Column(db.Float)
    yield_plant = db.Column(db.Float)
    yield_plot = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=Kampala_time)
    synced = db.Column(db.Boolean, default=False, nullable=False)


# --- 8. Yield (Greenhouse) ---
class YieldGreenhouseRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50))              # Added
    genotype = db.Column(db.String(100))
    replication = db.Column(db.String(20))
    greenhouse_id = db.Column(db.String(50))
    panicles = db.Column(db.Integer)
    panicle_length = db.Column(db.Float)
    filled_grains = db.Column(db.Integer)
    unfilled_grains = db.Column(db.Integer)
    grain_weight = db.Column(db.Float)
    yield_plant = db.Column(db.Float)
    yield_tray = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=Kampala_time)
    synced = db.Column(db.Boolean, default=False, nullable=False)


def create_tables():
    """Create all tables if they don’t exist."""
    db.create_all()
