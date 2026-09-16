import json,re,pathlib,hashlib,random
p=pathlib.Path(__file__).parent
a=json.loads((p/'screen.json').read_text(encoding='utf-8'))
def h(s,pat): return bool(re.search(pat,s,re.I))
for r in a:
 t=r['title']+' '+r['abstract']; title=r['title']
 real=h(t,r'firearms?|fire arms?|handguns?|pistols?|rifles?|gunshot|gunfire|weapons?|trigger guard|gun trigger|\bguns?\b')
 false=h(title,r'weld|spray|charg|massage|fascia|scanning|scan gun|oil(ing)? |filling|gluing|golf|launch monitor|electron |irradiat|combustor|automobile|paperboard|ceramic|pottery|barcode|bar.code|temperature measuring|nozzle|shotgun gate|weaponized')
 storage=h(t,r'cabinet|locker|vault|storage case|storage box|gun safe|gun rack|weapon rack|holster|storing weapons|storage receptacle')
 auth=h(t,r'authent|authoriz|biometr|fingerprint|biological (feature|characteristic)|biologic data|voice recognition')
 electronic=h(t,r'electronic|electrical|processor|sensor|smart|intelligent|wireless|RFID|GPS')
 data=h(t,r'track|traceability|logging|recording|collect|monitor|record.{0,30}(use|firing|shot)|usage')
 central=h(t,r'database|server|cloud|monitoring (center|station)|management cent')
 operate=h(t,r'(lock|unlock|disabl|enabl|prevent|permit).{0,60}(trigger|firing|firearm|shoot|discharge)|trigger.{0,25}lock')
 r['f']='AAAAAAAA'; r['lim']='No supported combination of firearm biometric authentication and firing control in the supplied text.'
 if false or not real:
  score=0; reason='Outside the disclosed firearm scope: '+title
 elif storage:
  score=12+4*auth+3*data+2*central; reason='Storage/access management; control of firearm firing is not established. '+title
 else:
  score=8+7*electronic+9*data+10*auth+10*operate+4*central
  score=min(score,54)
  reason=('Partial firearm relevance: '+', '.join(x for x,v in [('electronic systems',electronic),('identity/access features',auth),('operation-related control',operate),('tracking/data',data)] if v)+'. '+title)
 r['score']=score; r['reason']=reason[:310];r['explain']=reason[:310]

# Reviewed annotations are keyed to content-sorted candidate references, then saved by Record ID.
# Candidate positions and random IDs have no contribution to any relevance score.
def put(n,score,f,why,lim=''):
 r=a[n-1];r.update(score=score,f=f,reason=why,explain=why,lim=lim or 'Location-based restriction, central integration, use-purpose classification and danger-triggered unlocking are not established. Biometric acquisition does not establish usage logging.')
def core(nums,score=76,f='EEEAEAAA',lim=''):
 for n in nums:
  put(n,score,f,'Biometric user verification controls firearm firing or a firearm-attached safety lock. '+a[n-1]['title'],lim)
core([23,29,30,34,37,38,48,49,50,54,55,56,57,66,68,75,76,78,82,86,92,93,114,116,123,126,127,132,145,146,149,152,153,157,159,166,167,168,169,181,183,193,197,203,206,209,211,213,216,217,219,413,537])
core([31,32],75)
core([33,53,94,95,96,117,124,154,179],70,'EEIAEAAA', 'F3 is inferred from the biometric sensor/controller and firearm blocking mechanism described together; the authorization-to-release sequence is not fully stated. No location restriction or use-purpose classification is established.')
core([8,21,36,187,2529],62,'EEIAEAAA','F3 is inferred from a biometric gun lock intended to prevent unauthorized use; the exact firing-blocking interface is unclear. No geofencing or central database is established.')
put(194,96,'EEEE EAAA'.replace(' ',''),'Fingerprint matching and authorized-region checks jointly gate firearm unlocking, with position reporting and out-of-region alarms.','Alert destination and central/national database are unspecified. No use-purpose classification or danger-based unlocking.')
put(355,94,'EEEEEAAA','Biological-characteristic matching and geographic authorization jointly gate gun unlocking, with timely gun tracking.','Shooting-range application is not automatic classification of use purpose. Central database and danger-based unlocking are absent.')
for n in [7,15]: put(n,90,'EEEAEEAA','Fingerprint unlocking combines with firearm location and use-state monitoring through a public-security management website.','GPS collection and remote locking do not explicitly establish location-conditioned restriction. Alerts and use-purpose classification are not specified.')
put(165,89,'EEEAEEAA','Fingerprint verification controls the trigger linkage, with police-server communication and lost-gun positioning.','No explicit geographic firing restriction, use-purpose classification or physiological danger response.')
put(9,88,'EEEA EIAA'.replace(' ',''),'Authorized-user biometrics enable the trigger, and navigational data is transmitted to a weapon monitoring station.','F6 is inferred from navigational-data transmission to a monitoring station as central integration; a database and alerts are not stated. Geofencing is absent.')
for n in [13,18]: put(n,87,'EEEAEAAA','Fingerprint comparison controls the trigger lock, with automatic locking on loss of grip and real-time GPS reporting.','Mobile-terminal tracking does not establish a central database or geofenced firing restriction.')
put(20,86,'EEEAEAAA','Capacitive fingerprint verification gates pistol operation, with Beidou positioning, GSM communication and usage information.','No explicit central database, geofenced restriction or use-purpose classifier.')
put(1,85,'EEIE EEAA'.replace(' ',''),'Gun-mounted fingerprint authentication, locking components, tracking sensors and a law-enforcement/cloud connection are disclosed.','F3 is inferred from the gun-mounted authentication sensor and lock in a smart security control system; the release linkage is unstated. F4 is absent: GPS/proximity sensors alone do not establish location-based restriction.')
# Correct F4 to A: a GPS sensor is not a geofence.
a[0]['f']='EEIAEEAA'
put(16,85,'EEIAEEAA','Biometric access restriction accompanies firearm geolocation, event logging and cloud alerts for unauthorized activity.','F3 is inferred from authentication-restricted access in an integrated/retrofit firearm system; a firing interlock is not explicit. Event classification does not establish use-purpose classification.')
for n in [4,22]: put(n,84,'EEEAEAAA','Fingerprint authorization gates the firearm trigger and is combined with integrated location tracking.','Location detection does not establish geofenced operation. Central integration and use-purpose classification are absent.')
put(3,84,'EEEAEAAA','Fingerprint matching releases the gun safety latch, with satellite location and mobile connectivity.','Although titled a gun case, the abstract explicitly releases the gun safety latch. Location restriction and a central database are unstated.')
put(85,84,'EEEAEAAA','Biometric matching locks/unlocks the trigger, broadcasts unauthorized-use notifications and collects situational data on discharge.','Notification recipient and a central database are unspecified. No location restriction or automatic use-purpose classification.')
put(107,83,'EEEAEAAA','Fingerprint authentication permits weapon access and actuation while encrypted user-handling data is tracked in real time.','No location restriction or central/national database is established.')
put(105,82,'EEEAEAAA','Fingerprint-based firing authorization is combined with shot codes, image/audio recording and shot timing.','The abstract repeats its description and has translation ambiguity. No geofence, central integration or automatic purpose classifier.')
put(35,81,'EEEAEAAA','Fingerprint matching releases a trigger lock and unlock attempts and alerts are sent to a user device.','A user-device connection is not a centralized database. No geographic restriction or physiological danger unlocking.')
put(129,81,'EEIEEEAA','A firearm biometric authorization system uses server-assisted training and can register the firearm to its authorized user.','F3 is inferred from training whether the user is allowed to operate the firearm; a firing interlock is not described. Central server integration is explicit, but misuse alerts are not.')
put(90,81,'EEEAEAAA','Fingerprint-selective firing combines with permission-area tracking and alerts when the firearm leaves the area.','Leaving the area triggers a warning, not an explicit firing restriction. Central database not stated.')
put(113,79,'EEEAEIAA','Biometric identification, stored biometric data and a firearm-protector controller limit firearm use to specified users.','F6 is inferred from the linked electronic-information-device bank and data transmission; a central/national service or alerts are not explicit. Translation is unclear.')
put(115,80,'EEEAEAAA','Biometric sensing, authorized-user control and mental-state evaluation condition release of the trigger interlock.','F8 is absent: acceptable mental state is not immediate-danger detection followed by unlocking. No geofence or central database.')
put(58,79,'EEEAEAAA','Registered fingerprints enable firing, with a biometric database and tamper detection.','Database locality is unspecified, so F6 is absent. Claimed traceability lacks a concrete usage-log mechanism.')
for n in [512,620]: put(n,79,'EEEA EIAA'.replace(' ',''),'Biological user verification and remote-server authorization control an electronic firearm lock, with motion-state sensing.','F6 is inferred from remote-server authorization, but central database storage and alerts are not stated. No location restriction.')
put(17,74,'EEEAEAAA','Fingerprint matching with normal temperature/pulse conditions enables unlocking of weapon controls.','Broad weapon/transport control covers rather than a detailed firearm implementation. Normal pulse validation is not danger-triggered unlocking.')
put(212,75,'EEEAEAAA','The gun includes facial/fingerprint or PIN locking and unauthorized-user alarms.','AI friend/foe targeting is excluded from scoring. No geofence or central database is established.')
put(52,71,'EEIAEAAA','A grip-mounted biometric skin sensor determines whether a user is authorized to discharge an electronic firearm.','F3 is inferred from determining authorization to discharge; the mechanism enforcing that result is not described.')
put(51,65,'EEIAAAAA','A smart-gun fingerprint securing device checks sequential authorizations.','F3 is inferred from firearm securing by authorization checks; trigger blocking and sensor data collection details are absent from the abstract.')
put(130,69,'EEIAAAAA','A biometric gun lock encloses the trigger and uses a microcontroller-driven release mechanism.','F3 is inferred from the biometric lock title and trigger-enclosing release mechanism; explicit user matching is absent.')
put(645 if False else 190,74,'EEEAEAAA','Fingerprint and facial verification unlock a magazine that otherwise blocks loading/unloading of bullets.','Controls ammunition availability rather than a direct trigger interlock. No location restriction or central database.')
put(208,64,'EEIAEAAA','Firearm safety personalization combines biometric authentication, localization and wireless connectivity.','F3 is inferred from biometric personalization in a firearm safety device; the lock-control sequence is unspecified. Localization is not a geofence.')
put(195,55,'EEIAAAAA','The title describes an external weapon lock using biometric scanning.','Abstract is only "1818". F3 is inferred from the biometric external-lock title; firing control and implementation are unclear.')
put(138,56,'EEIAEAAA','A fingerprint verifier and controller operate locks in an assault rifle.','F3 is inferred only for authorized mechanical operation; the described locks concern fixing/dismounting rather than clearly preventing firing.')
put(28,54,'EEAAEEAA','A firearm sight collects biometric information and communicates with a remote command center for authentication.','No authentication-dependent firing lock is stated. Center data processing/storage is explicit; alerts are not.')
put(109,52,'EEIAEAAA','User authentication selects stored settings for gun peripherals.','F3 is inferential only for peripheral operation from authentication-dependent configuration; discharge prevention is not disclosed. Haptic benefits are excluded.')
for n in [150,151,191]: put(n,60,'EEEAEAAA','Fingerprint authorization restricts operation of a projectile/electrical stun weapon.','Electrical stun weapon rather than the central conventional-firearm embodiment. No geofence or central database.')
for n in [253,254]: put(n,88,'EIEEEAAA','User identity verification gates discharge and GPS/time restrictions disable firearms in prohibited areas.','F2 is inferred from a microphone verifying user identity as voice-biometric recognition; the recognition method is unspecified. Features are optional embodiments. No central database.')
put(249,73,'EAEEEEAA','Electronic user authorization and GPS-based prohibited-area trigger locking link to multiple management databases.','Biometric authentication is not stated. No use-purpose classification or danger-based unlocking.')
put(297,65,'EAAEEIAA','A server uses weapon location and projected travel path to send a disabling instruction.','F6 is inferred from server integration, without explicit database/alert disclosure. No biometric or user-authentication-dependent control.')
put(588,66,'EAEEEIAA','A server checks gun and location permission data before authorizing release of the gun lock.','F6 is inferred from server-stored permission information; central alerts are not stated. No biometric authentication.')
put(256,56,'EAAIAAAA','Weapon sensors condition firing-sequence release on safe location, environment and situation.','F4 is inferred from safe-location sensing as a condition of unlocking; geographic boundaries are unspecified. No user biometrics. Excluded target-assessment concepts receive no credit.')
put(345,67,'EA EAEAAA'.replace(' ',''),'Matching authorized-user and operation data unlocks firing, with camera evidence and continuous user-data collection.','The identity data modality is unspecified, so biometric identification is not established.')
put(274,63,'EAEAEAAA','A remote authority authenticates operators, receives location/video/use information and authorizes or deauthorizes firing.','No biometric method, database or automatic location-conditioned restriction is stated.')
put(422,62,'EAEAEAAA','Smart firearm components recognize authorized users, control operations, track inventory and communicate status alerts.','Voice commands do not establish voice-biometric authentication. Remote devices do not establish a central database.')
put(501,61,'EAEAEAAA','Authorized-person firing protection accompanies stored sounds, firing times and firearm positions.','Authentication modality and enforcement details are sparse. No central database or geofenced restriction.')
put(351,60,'EA EAEAAA'.replace(' ',''),'User profile sensors are compared with authorized-profile data to command a gun-lock actuator.','Profile information is not explicitly biometric. Database locality is unspecified.')
put(442,60,'EAEAEAAA','Enrollment-data matching at gun authentication sensors enables an active state allowing firing.','Sensor modalities are unspecified, so biometrics are not established. No location restrictions or central integration.')
put(311,58,'EAEAEAAA','An electromagnetic sensor and grip computing device permit firing when received radiation corresponds to an authorized user.','No explicit biometric source for the electromagnetic signal; a token is also possible. Charging concepts receive no credit.')
for n in [298,335,339,500,522,530,540,630,660,669,829]:
 put(n,57,'EAEAAAAA','Authorized-user or credential verification controls firearm operation. '+a[n-1]['title'],'Biometric identification is not established. No geographic firing restriction or central usage database is shown.')
put(245,55,'EAIAEAAA','A magazine-well device tracks location and status and renders the firearm non-functional.','F3 is inferred from limiting unauthorized use by a secured blocking device; the authentication/release mechanism is not stated.')
put(257,50,'EAIAEAAA','An attached security device renders an object unusable and provides location and sensor-data transmission, including for firearms.','F3 is inferred from the locking/disengagement mechanism; user authentication is unspecified. Broad multi-object disclosure.')
put(382,53,'EAIAEEAA','Smart firearms send shot information to a center retaining communication history and receive remote-inhibition instructions.','F3 is inferred from remote inhibition; user-authentication gating is not explicit. No biometrics or geographic restriction.')
put(263,47,'EAAAEEAA','Gun-identified shot events yield location/time use-of-force reports stored in a remote database.','Use-of-force reporting is not automatic classification among self-defence/recreation/other purposes. No firing authorization.')
put(2396,46,'EAAAEEAA','Gun-installed electronics report to a background information database for use-process tracking and early warning.','No explicit biometric authorization or firing lock.')
put(385,45,'EIAAEAAA','Firearm telemetry identifies who fired from unique trigger-pull behavior and transmits firing information.','F2 is inferred as behavioral-biometric identification from unique individual trigger-pull signatures; pre-use authorization is absent.')
put(12,44,'EAAAEAAA','Firearm-mounted/wearable sensors classify and record shot events, with external synchronization.','Biometric inputs are not used for authorized-user identification. Shot classification is not use-purpose classification.')
put(224,42,'EAAAEAAA','Weapon/holster activation sensing transmits discharge and user-biometric-state information.','Biometric state supports predictive diagnosis, not identity authentication or danger-conditioned unlocking.')
put(791,40,'EAAAEAAA','Firearm motion-event data is compared with stored patterns to determine a user state.','Fatigue/state detection is not authorization, use-purpose classification or danger-triggered unlocking.')
put(695,43,'EAAAEAAA','Smart-gun sensors log shooting behavior with time and location.','Shooting-event detection does not establish use-purpose classification. No biometric firing authorization.')
put(842,46,'EAAAEIAA','Gun-installed identity verification accompanies usage recording and transmission to a host controller.','F6 is inferred from a common host controller receiving gun records; a central database and alerts are not explicit. No firing interlock or biometric modality.')

for n in [94,95]:
 a[n-1]['f']='EIIAEAAA'
 a[n-1]['lim']='F2 and F3 are inferred from a rifle-mounted biometric sensor whose data actuates the blocking mechanism, suggesting user-specific permission; enrolled-user matching is not explicit. No location restriction or central integration.'
# Collection is credited only when a sensing, reading, input or stored-data mechanism is stated.
for r in a:
 if r['f'][4]=='E' and not h(r['title']+' '+r['abstract'],r'sensor|sens(e|es|ing)|scan|read|collect|gather|inductor|record|track|tracing|data|information|memory|stor|GPS|location|position|microphone|fingerprint recogn|biometric recogn|fingerprint identif|biometric identif'):
  r['f']=r['f'][:4]+'A'+r['f'][5:]
 def clarity(text):
  return sum(bool(re.search(pat,text,re.I)) for pat in [r'(only|when|if|based on|according to|in response).{0,100}(authoriz|fingerprint|biometr|match|recogn)',r'(lock|unlock|disabl|enabl|prevent|permit).{0,70}(trigger|firing|discharg)',r'(fingerprint|biometr).{0,90}(compar|match|authoriz)',r'(trigger|firing mechanism).{0,60}(lock|unlock|disabl|enabl)'])
 r['clarity']=clarity(r['abstract'])
# Equal content/evidence receives equal scores; a random lottery resolves exact content ties.
random.SystemRandom().shuffle(a)
ranked=sorted(a,key=lambda r:(-r['score'],-sum(2 if z=='E' else 1 if z=='I' else 0 for z in r['f'][1:5]),-r['clarity'],-r['f'].count('E'),r['title'].casefold(),r['abstract']))
# For textually identical records the score and evidence are equal; content ties are interchangeable.
for i,r in enumerate(ranked):
 r['rank']=i+1;r['category']='H' if r['score']>=75 else 'M+' if r['score']>=55 else 'M' if r['score']>=30 else 'L' if r['score']>=10 else 'N'
 assert len(r['f'])==8,(r['title'],r['f'])
 if i<100:
  parts=re.split(r'(?<=[.!?])\s+',r['abstract'])
  def val(s):return sum(bool(re.search(pat,s,re.I)) for pat in [r'finger|biometr|biolog|iris|voice',r'lock|unlock|firing|discharg|authoriz',r'geograph|GPS|position|location|region',r'track|record|collect|data',r'database|server|cloud|alert|monitor'])
  best=sorted(sorted(range(len(parts)),key=lambda j:-val(parts[j]))[:4])
  snippets=[]
  for j in best:
   s=parts[j]
   if len(s)>550:
    m=re.search(r'fingerprint|biometr|biolog|authoriz|GPS|geograph|lock|track',s,re.I)
    start=max(0,(m.start() if m else 0)-60)
    s=('…' if start else '')+s[start:start+550]+'…'
   snippets.append(s)
  r['evidence']='Title: '+r['title']+'\nAbstract excerpts: '+' … '.join(snippets)
  if r['abstract']=='1818':r['evidence']='Title: '+r['title']+'\nAbstract: 1818 (no usable technical description).'
(p/'ranked.json').write_text(json.dumps(ranked,ensure_ascii=False,indent=2),encoding='utf-8')
assert {r['id'] for r in ranked}=={r[0] for r in json.loads((p/'input.json').read_text(encoding='utf-8'))[1:]}
print('\n'.join(f"{r['rank']} {r['score']} {r['f']} {r['title']}" for r in ranked[:110]))
print('COUNTS', {k:sum(r['category']==k for r in ranked) for k in ['H','M+','M','L','N']})
