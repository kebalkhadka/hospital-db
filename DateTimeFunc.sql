-- Find the age (in years) of each patient as of today.
-- timestampdiff is used as we will also count if a  person reached through month or not.
Select 
p.full_name as patient_name,
timestampdiff(Year,date_of_birth,current_date()) as age
from 
patients p;

-- List doctors who joined the hospital more than 5 years ago.

select 
d.full_name as doctor_name
from 
doctors d
where 
Year(current_date()) - year((joining_date)) > 5;

-- List all patients along with the medicines prescribed to them in the last 6  month.
select 
p.patient_id,p.full_name as patinet_name,
pr.medicine_name 
from 
patients p 
join 
appointments a on p.patient_id = a.patient_id
join 
prescriptions pr on a.appointment_id = pr.appointment_id
where a.appointment_date >= date_sub(curdate(), interval 6 month);



-- Find a patient who had a appointment but no prescription was issued 
select distinct p.full_name 
from 
patients p 
join 
appointments a on p.patient_id = a.patient_id
left join 
prescriptions pr on a.appointment_id = pr.appointment_id
where 
pr.appointment_id is null;




-- List all doctors who have more appointments than the average number of appointments per doctor
select 
d.full_name,
count(a.appointment_id) as total_appointment
from 
doctors d 
join 
appointments a 
on d.doctor_id = a.doctor_id
group by d.doctor_id,d.full_name
having count(a.appointment_id)>(
select 
avg(appointment_count)
from(
select count(*) as appointment_count
from appointments
group by doctor_id)as t
);