CREATE TABLE table_m3 (
	"Marital status" INT,
	"Application mode" INT,
	"Application order" INT,
	"Course" INT,
	"Daytime/evening attendance\t" INT,
	"Previous qualification" INT,
	"Previous qualification (grade)" FLOAT,
	"Nacionality" INT,
	"Mother's qualification" INT,
	"Father's qualification" INT,
	"Mother's occupation" INT,
	"Father's occupation" INT,
	"Admission grade" FLOAT,
	"Displaced" BOOLEAN,
	"Educational special needs" BOOLEAN,
	"Debtor" BOOLEAN,
	"Tuition fees up to date" BOOLEAN,
	"Gender" BOOLEAN,
	"Scholarship holder" BOOLEAN,
	"Age at enrollment" INT,
	"International" BOOLEAN,
	"Curricular units 1st sem (credited)" FLOAT,
	"Curricular units 1st sem (enrolled)" FLOAT,
	"Curricular units 1st sem (evaluations)" FLOAT,
	"Curricular units 1st sem (approved)" FLOAT,
	"Curricular units 1st sem (grade)" FLOAT,
	"Curricular units 1st sem (without evaluations)" FLOAT,
	"Curricular units 2nd sem (credited)" FLOAT,
	"Curricular units 2nd sem (enrolled)" FLOAT,
	"Curricular units 2nd sem (evaluations)" FLOAT,
	"Curricular units 2nd sem (approved)" FLOAT,
	"Curricular units 2nd sem (grade)" FLOAT,
	"Curricular units 2nd sem (without evaluations)" FLOAT,
	"Unemployment rate" FLOAT,
	"Inflation rate" FLOAT,
	"GDP" FLOAT,
	"Target" VARCHAR(255)
);

SELECT * FROM public.table_m3;

-- Saat menambahkan data ini dilakukan menggunakan psql
COPY table_m3( "Marital status","Application mode","Application order","Course","Daytime/evening attendance\t","Previous qualification
","Previous qualification (grade)","Nacionality","Mother's qualification","Father's qualification","Mother's occupation","Father's occupation","A
dmission grade","Displaced","Educational special needs","Debtor","Tuition fees up to date","Gender","Scholarship holder","Age at enrollment","Int
ernational","Curricular units 1st sem (credited)","Curricular units 1st sem (enrolled)","Curricular units 1st sem (evaluations)","Curricular unit
s 1st sem (approved)","Curricular units 1st sem (grade)","Curricular units 1st sem (without evaluations)","Curricular units 2nd sem (credited)","
Curricular units 2nd sem (enrolled)","Curricular units 2nd sem (evaluations)","Curricular units 2nd sem (approved)","Curricular units 2nd sem (gr
ade)","Curricular units 2nd sem (without evaluations)","Unemployment rate","Inflation rate","GDP","Target")
FROM 'C:\M3\table_m3.csv'
WITH DELIMITER ';' CSV HEADER;