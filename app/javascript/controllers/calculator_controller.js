import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
    static targets = ["newTermField", "closingCostsField"]

    connect() {
        console.log("Calculator connected")
    }

    toggleTerm() {
        console.log("Term toggled")
    }

    toggleClosingCosts() {
        console.log("Closing costs toggled")
    }
}