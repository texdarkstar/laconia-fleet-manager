import { integer, pgEnum, pgTable, varchar } from "drizzle-orm/pg-core";
import { shipClassifications } from "../types/shipClassification";

// You're not using enums but this is how I'd do it.
export const PgShipClassification = pgEnum(
    'ship_classification', 
    // Just doing this to so you don't have to define the classifications twice
    shipClassifications.map(({acronym}) => acronym) as [string, ...string[]] 
);

export const ShipModelTable = pgTable('ship_model', {
    id: integer('id').primaryKey().generatedAlwaysAsIdentity({startWith: 1}),
    name: varchar('name').notNull(),
    designer: varchar('designer').notNull(), // Discord ID of the designer
    //classification: PgShipClassification('classification').notNull(), // Not using enums but this is how you'd do it
    classification: varchar('classification').notNull(),
});

export const ShipyardTable = pgTable('shipyard', {
    id: integer('id').primaryKey().generatedAlwaysAsIdentity({startWith: 1}),
    name: varchar('name').notNull(),
    owner: varchar('owner').notNull(), // Discord ID of the owner
});

export const ShipTable = pgTable('ship', {
    id: integer('id').primaryKey().generatedAlwaysAsIdentity({startWith: 1}),
    name: varchar('name').notNull(),
    modelId: integer('model_id').references(() => ShipModelTable.id).notNull(),
    shipyardId: integer('shipyard_id').references(() => ShipyardTable.id).notNull(),
    assignedTo: varchar('assigned_to'), // Discord ID of the assigned user
    status: varchar('status'),
    location: varchar('location'),
});
