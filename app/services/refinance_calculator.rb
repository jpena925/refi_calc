class RefinanceCalculator
  attr_reader :current_balance, :current_rate, :years_remaining, :current_payment,
              :new_rate, :same_term, :new_term_years, :new_term_months, :remaining_months,
              :used_estimate, :closing_costs, :closing_costs_low, :closing_costs_mid, :closing_costs_high,
              :new_payment, :monthly_savings, :annual_savings,
              :break_even_months, :break_even_years, :break_even_remaining_months,
              :total_current_cost, :total_new_cost, :total_current_interest, :total_new_interest,
              :interest_savings, :total_payment_savings, :net_savings, :recommendation

  def initialize(params)
    @current_balance = params[:current_balance].to_f
    @current_rate = params[:current_rate].to_f
    @years_remaining = params[:years_remaining].to_i
    @current_payment = params[:current_payment].to_f
    @new_rate = params[:new_rate].to_f
    @same_term = params[:same_term] == "1"
    @new_term_years = @same_term ? @years_remaining : params[:new_term].to_i
    @new_term_months = @new_term_years * 12
    @remaining_months = @years_remaining * 12
    @used_estimate = params[:knows_closing_costs] == "1"

    calculate_closing_costs(params)
  end

  def calculate
    calculate_new_payment
    calculate_savings
    calculate_break_even
    calculate_interest
    calculate_net_savings
    generate_recommendation
    self
  end

  private

  def calculate_closing_costs(params)
    if @used_estimate
      @closing_costs_low = @current_balance * 0.02
      @closing_costs_mid = @current_balance * 0.03
      @closing_costs_high = @current_balance * 0.05
      @closing_costs = @closing_costs_mid
    else
      @closing_costs = params[:closing_costs].to_f
    end
  end

  def calculate_new_payment
    @new_payment = monthly_payment(@current_balance, @new_rate, @new_term_months)
  end

  def calculate_savings
    @monthly_savings = @current_payment - @new_payment
    @annual_savings = @monthly_savings * 12
  end

  def calculate_break_even
    return unless @monthly_savings > 0

    @break_even_months = @closing_costs / @monthly_savings
    @break_even_years = (@break_even_months / 12).to_i
    @break_even_remaining_months = (@break_even_months % 12).to_i
  end

  def calculate_interest
    @total_current_cost = @current_payment * @remaining_months
    @total_new_cost = @new_payment * @new_term_months
    @total_current_interest = @total_current_cost - @current_balance
    @total_new_interest = @total_new_cost - @current_balance
    @interest_savings = @total_current_interest - @total_new_interest
  end

  def calculate_net_savings
    @total_payment_savings = @monthly_savings * @remaining_months
    @net_savings = @total_payment_savings - @closing_costs
  end

  def generate_recommendation
    @recommendation = if @monthly_savings <= 0
      {
        status: :not_recommended,
        icon: "❌",
        title: "NOT RECOMMENDED",
        message: "This refinance would increase your monthly payment. Unless you specifically want to shorten your loan term, this refinance may not make sense."
      }
    elsif @break_even_months <= 24
      {
        status: :strongly_recommended,
        icon: "✅",
        title: "STRONGLY RECOMMENDED",
        message: "You'll break even in just #{format_break_even}! After that, you're saving #{format_currency(@monthly_savings)}/month. If you plan to stay in the home more than 2 years, this is a great deal."
      }
    elsif @break_even_months <= 48
      {
        status: :recommended,
        icon: "✅",
        title: "RECOMMENDED",
        message: "Break-even period: #{format_break_even}. This makes sense if you plan to stay in the home at least 4 years. The longer you stay, the more you save."
      }
    elsif @break_even_months <= 84
      {
        status: :consider,
        icon: "⚠️",
        title: "CONSIDER CAREFULLY",
        message: "Break-even period: #{format_break_even}. This only makes sense if you're confident you'll stay in the home for at least #{(@break_even_months / 12).to_i + 1} years."
      }
    else
      {
        status: :not_worth_it,
        icon: "❌",
        title: "PROBABLY NOT WORTH IT",
        message: "Break-even period: #{format_break_even}. The savings are too small relative to closing costs. Consider negotiating lower closing costs or waiting for a better rate."
      }
    end
  end

  def monthly_payment(principal, annual_rate, months)
    return principal / months if annual_rate == 0 || months == 0

    monthly_rate = annual_rate / 100.0 / 12
    principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
  end

  def format_break_even
    return "N/A" unless @break_even_months

    if @break_even_years == 0
      "#{@break_even_remaining_months} months"
    elsif @break_even_remaining_months == 0
      "#{@break_even_years} years"
    else
      "#{@break_even_years} years, #{@break_even_remaining_months} months"
    end
  end

  def format_currency(amount)
    ActionController::Base.helpers.number_to_currency(amount)
  end
end
