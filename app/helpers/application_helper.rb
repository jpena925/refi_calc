module ApplicationHelper
  def recommendation_bg_class(status)
    case status
    when :strongly_recommended, :recommended
      "bg-green-100 border border-green-300"
    when :consider
      "bg-yellow-100 border border-yellow-300"
    when :not_recommended, :not_worth_it
      "bg-red-100 border border-red-300"
    else
      "bg-gray-100"
    end
  end
end
