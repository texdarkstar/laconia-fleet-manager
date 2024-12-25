CREATE TYPE "public"."ship_classification" AS ENUM('CC', 'CA', 'FF', 'DDG');--> statement-breakpoint
CREATE TABLE "ship_model" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "ship_model_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"name" varchar NOT NULL,
	"designer" varchar NOT NULL,
	"classification" varchar NOT NULL
);
--> statement-breakpoint
CREATE TABLE "ship" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "ship_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"name" varchar NOT NULL,
	"model_id" integer NOT NULL,
	"shipyard_id" integer NOT NULL,
	"assigned_to" varchar,
	"status" varchar,
	"location" varchar
);
--> statement-breakpoint
CREATE TABLE "shipyard" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "shipyard_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"name" varchar NOT NULL,
	"owner" varchar NOT NULL
);
--> statement-breakpoint
ALTER TABLE "ship" ADD CONSTRAINT "ship_model_id_ship_model_id_fk" FOREIGN KEY ("model_id") REFERENCES "public"."ship_model"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "ship" ADD CONSTRAINT "ship_shipyard_id_shipyard_id_fk" FOREIGN KEY ("shipyard_id") REFERENCES "public"."shipyard"("id") ON DELETE no action ON UPDATE no action;