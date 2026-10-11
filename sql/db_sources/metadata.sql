
create  table metadata ( 
    machine_id serial primary key,
    temperature float ,
    vibration float ,
    rpm float , 
    status varchar(100) ,
    measured_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
); 


