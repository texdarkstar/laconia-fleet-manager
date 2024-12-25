export const shipClassifications: ShipClassification[] = [
    {
        name: "Cruiser", // no idea what the actual ship classifications are
        acronym: "CC"
    },
    {
        name: "Gun Cruiser",
        acronym: "CA"
    },
    { 
        name: "Frigate",
        acronym: "FF"
    },
    {
        name: "Guided Missile Destroyer",
        acronym: "DDG"
    }
]

export type ShipClassification = {
    name: string,
    acronym: string,
}