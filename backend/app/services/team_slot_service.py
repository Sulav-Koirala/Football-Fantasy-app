from app.models.Team_models import FormationEnum
from sqlalchemy.orm import Session
from app.repository import team_slot_repo

POSITION_LIMITS = {
     "GK": 2,
     "DF": 5,
     "MF": 5,
     "FW": 3
}
FORMATION_LIMITS = {
    "3-5-2": {"GK": 1, "DF": 3, "MF": 5, "FW": 2},
    "3-4-3": {"GK": 1, "DF": 3, "MF": 4, "FW": 3},
    "4-5-1": {"GK": 1, "DF": 4, "MF": 5, "FW": 1},
    "4-4-2": {"GK": 1, "DF": 4, "MF": 4, "FW": 2},
    "4-3-3": {"GK": 1, "DF": 4, "MF": 3, "FW": 3},
    "5-4-1": {"GK": 1, "DF": 5, "MF": 4, "FW": 1},
    "5-3-2": {"GK": 1, "DF": 5, "MF": 3, "FW": 2},
    "5-2-3": {"GK": 1, "DF": 5, "MF": 2, "FW": 3}
}

def assign_slots(db: Session, team_formation: FormationEnum, user_id: int):
    slots= []
    slot_no = 1
    for position, max_count in POSITION_LIMITS.items():
        for _ in range(max_count):
            if slot_no == 1:
                role = "Captain"
            elif slot_no == 3:
                role = "Vice Captain"
            else: 
                role = "Member"

            slots.append({
                "team_id": user_id,
                "slot_no": slot_no,
                "slot_position": position,
                "slot_status": "Bench",  
                "slot_role": role
            })
            slot_no += 1
    team_slot_repo.assign_slots(db,slots)

    starters = FORMATION_LIMITS[team_formation.value]
    for pos,count in starters.items():
        position_count =  team_slot_repo.get_slot_details(db,user_id,pos)
        for index, slot_obj in enumerate(position_count):
            slot_obj.slot_status = "Starting" if index < count else "Bench"
    team_slot_repo.commit(db)

def arrange_slots(db: Session, team_formation : FormationEnum, user_id: int):
    try:
        team_slot_repo.delete_slots(db,user_id)
        assign_slots(db, team_formation, user_id)
        team_slot_repo.commit(db)
    except Exception:
        team_slot_repo.rollback(db)
        raise