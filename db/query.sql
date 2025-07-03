drop schema webai;
create schema webai;
use webai;

create table users (
	id int auto_increment primary key,
    username varchar(50) not null,
    email varchar(100) not null unique,
    hashed_password varchar(256) not null,
    full_name varchar(50),
    phone_number varchar(10),
	is_active bool default true, #allow or remove activity
    role enum('user', 'admin') default 'user',
    created_at datetime default current_timestamp
    );
    
create table sessions (
	id int auto_increment primary key,
    user_id int not null,
    device_id int not null,
    is_active bool default true, #check the device's session is allowed
    created_at datetime default current_timestamp,
    last_active_at datetime default current_timestamp on update current_timestamp,
    
    foreign key (user_id) references users(id) on delete cascade
    );
    
create table device_info (
	id int auto_increment primary key,
    user_id int not null,
    device_fingerprint text,
    first_seen datetime default current_timestamp,
    last_seen datetime,
    ip_address varchar(45),
    
    foreign key (user_id) references users(id) on delete cascade
    );
    
alter table sessions 
add foreign key (device_id) references device_info(id) on delete cascade