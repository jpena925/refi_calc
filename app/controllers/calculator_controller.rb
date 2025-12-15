class CalculatorController < ApplicationController
  def index
  end

  def calculate
    @result = RefinanceCalculator.new(params).calculate
    render :results
  end
end
