# TODO List for Flask API Implementation

## 1. Update server/models.py
- [x] Add relationships: signups in Camper and Activity, camper_id and activity_id in Signup
- [x] Add validations: Camper (name required, age 8-18), Signup (time 0-23)
- [x] Set serialization rules to limit recursion
- [x] Configure cascade deletes for Signup

## 2. Update server/app.py
- [x] Instantiate Api class
- [x] Define Resource classes for routes: Campers, CamperById, Activities, ActivityById, Signups
- [x] Add routes using api.add_resource

## 3. Run migrations and seed
- [x] flask db migrate -m 'implement relationships'
- [x] flask db upgrade head
- [x] python seed.py

## 4. Test
- [x] Run pytest -x to verify implementation
