import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
    static targets = ["newTermField", "closingCostsField"]

    connect() {
        console.log("Calculator connected")
    }

    toggleTerm() {
        this.newTermFieldTarget.classList.toggle("hidden")
    }

    toggleClosingCosts() {
        this.closingCostsFieldTarget.classList.toggle("hidden")
    }
}