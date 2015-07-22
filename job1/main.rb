#!/usr/bin/ruby -w
require 'csv'

$train_file_content = CSV.read('train_1_5.csv', converters: :float)
$test_file_content = CSV.read('test_1_5.csv', converters: :float)

$init_para = [0.0, 0.0, 0.0]

def sign(row, para)
    (para[0] * row[0] + para[1] * row[1] + para[2]) >= 0 ? 1.0 : -1.0
end

def errors(para)
    $train_file_content.select { |row| sign(row, para) != row[2] }.size
end

def predict_errors(para)
    $test_file_content.select { |row| sign(row, para) != row[2] }.size
end

def patch(para, row)
    [
        para[0] + row[2] * row[0],
        para[1] + row[2] * row[1],
        para[2] + row[2]
    ]
end

def analysis(para)
    $train_file_content.map { |row| patch(para, row) if (sign(row, para) != row[2]) }.compact
end

def deepin(now, para, depth)
    if now < depth
        results = analysis(para).map { |sub_para| deepin(now+1, sub_para, depth) }

        this_errors = results.map { |result| result[0] }
        this_para = results.map { |result| result[1] }

        this_errors.push(errors(para))
        this_para.push(para)
    else
        this_para = analysis(para)
        this_para.push(para)

        this_errors = this_para.map { |m_para| errors(m_para) }
    end

    this_error_min = this_errors.min
    [this_error_min, this_para[this_errors.index(this_error_min)]]
end

$final_result = deepin(0, $init_para, 1)
$best_errors = $final_result[0]
$best_para = $final_result[1]
$prediction_errors = predict_errors($best_para)

puts("Best errors: #{$best_errors}, prediction errors: #{$prediction_errors}, best para: #{$best_para}")
