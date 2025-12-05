-- Show prescriptions where the duration_days is greater than the average duration in the entire Prescriptions table. (correlated subquery possible)

Select * from prescriptions
where
duration_days > (select avg(duration_days) from prescriptions);


-- Rank patients by their total number of appointments (descending). Show patient name and rank. 
select 
p.full_name,
t.total_appointment,
rank() over(order by t.total_appointment desc) as rnk
from(
select 
patient_id,
count(*) as total_appointment
from 
appointments
group by patient_id) t
join
patients p 
on p.patient_id = t.patient_id
order by rnk desc;


-- Show running total (cumulative) of appointments day by day

select p.full_name,
a.appointment_id,
a.appointment_date,
count(*) over( 
partition by a.patient_id
order by a.appointment_date
rows between unbounded preceding and 1 preceding) as prev_appointment
from 
patients p
join 
appointments a 
on 
p.patient_id = a.patient_id ;


-- For each appointment, show how many appointments that patient had before this one.
select 
a.patient_id,
a.appointment_id,
count(*) over(partition by a.patient_id order by a.appointment_date rows between unbounded preceding and 1 preceding) as prev
from 
appointments a ;


-- Find the top 3 patients with the highest number of appointments.

select * from 
(
select 
p.full_name,
dense_rank() over(order by total_appointment desc)as rnk
from (
	select patient_id,
    count(*) as total_appointment
    from 
    appointments
    group by patient_id
)t
join patients p 
on p.patient_id = t.patient_id
)x
where rnk <=3;


--  For each doctor, show the top 2 most frequent patients.
Select * from (
select 
doctor_id,patient_id,no_of_visit,
dense_rank() over(partition by doctor_id order by no_of_visit) as rnk
from(
	select doctor_id,patient_id,
    count(*) as no_of_visit
    from 
    appointments
    group by doctor_id,patient_id
)t 
) x
where rnk<=2 order by doctor_id,rnk;

-- Show the most expensive 3 tests based on cost
select 
test_name,cost,rnk
from(
select
test_name,cost,
 dense_rank() over(order by cost desc ) as rnk 
from medicaltests
)t
where  rnk <=3
order by rnk;


