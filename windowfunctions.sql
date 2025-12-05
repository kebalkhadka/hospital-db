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



