#!/usr/bin/ruby -w

require 'csv'
require 'json'

$train_set = CSV.read('trainfeat.txt', col_sep: ' ', converters: :float)
$train_label = CSV.read('trainlabs.txt', col_sep: ' ', converters: :float).flatten!
$test_set = CSV.read('testfeat.txt', col_sep: ' ', converters: :float)
$test_label = CSV.read('testlabs.txt', col_sep: ' ', converters: :float).flatten!

$data_pack = $train_set.zip($train_label).shuffle!
$train_pack = $data_pack[5000..($data_pack.length - 5000)]
$validation_pack = $data_pack[0..5000]

$train_set, $train_label = $train_pack.transpose
$validation_set, $validation_label = $validation_pack.transpose

$data_pack = nil
$train_pack = nil
$validation_pack = nil

def entropy(first, second)
	if first == 0 || second == 0
		-Math.log2(1)
	else
		fp = first.to_f / (first + second)
		sp = 1 - fp
		-(fp * Math.log2(fp) + sp * Math.log2(sp))
	end
end

class Node
	def initialize(data, label, feature, feature_index = nil, feature_value = nil, flag = nil)
		@data = data
		@label = label
		@feature = feature
		@feature_index = feature_index
		@feature_value = feature_value
		@flag = flag
		@childs = {}

		if flag == nil
			puts('HERE')
			@features = data.first.length
			@samples = data.length
			@trues = label.reduce(:+).to_i
			#@entropy = entropy(@trues, @samples - @trues)

			#print("Sample: #{@samples}, Feature: #{@features}, Trues: #{@trues}, FeatureIndex: #{@feature_index}, FeatureValue: #{@feature_value}\n")
			if @samples > 1 && @features > 1 && @trues != 0 && @trues != @samples
				prepare
				prepare_true
				grow
			else
				if @samples >= (2 * @trues)
					@flag = false
				else
					@flag = true
				end
			end
		else
			#print("FeatureIndex: #{@feature_index}, FeatureValue: #{@feature_value}, Flag: #{@flag}\n")
		end

		@data = nil
		@label = nil
		@feature = nil
	end

	def prepare
		table = []

		(0...@features).each do |f|
			table.push({})
			(0...@samples).each do |r|
				if table[f][@data[r][f]] == nil
					table[f][@data[r][f]] = 1
				else
					table[f][@data[r][f]] += 1
				end
			end
		end

		@table = table
	end

	def prepare_true
		table = []

		(0...@features).each do |f|
			table.push({})
			(0...@samples).each do |r|
				if table[f][@data[r][f]] == nil
					table[f][@data[r][f]] = 0
				end

				if @label[r] == 1
					table[f][@data[r][f]] += 1
				end
			end
		end

		@true_table = table
	end

	def index_to_entropy(index)
		aggregate = 0.0
		weight_sum = 0.0

		if @table[index] == nil
			print("In entropy: Length: #{@table.length}, Index: #{index}\n")
		end
		@table[index].each do |key, value|
			true_value = @true_table[index][key]
			new_entropy = entropy(value - true_value, true_value)
			aggregate += new_entropy * value
			weight_sum += value
		end

		aggregate / weight_sum
	end

	def grow
		#key -> global_feature_index
		#index -> local_feature_index

		min_entropy = Float::INFINITY
		local_feature_index = 0

		new_index = 0
		new_rule_index = 0

		@feature.each do |key, value|
			if value
				new_entropy = index_to_entropy(local_feature_index)

				if new_entropy < min_entropy
					min_entropy = new_entropy
					new_index = local_feature_index
					new_rule_index = key
				end

				local_feature_index += 1
			end
		end
		
		@rule_index = new_rule_index

		#print(min_entropy, new_index, new_rule_index)
		#print(@table[new_index])
		#print(@trueTable[new_index])
		#print(@entropy, min_entropy)

		child_feature = @feature.clone
		child_feature[new_rule_index] = false

		if @table[new_index] == nil
			print("Length: #{@table.length}, Index: #{new_index}\n")
		end
		if @table[new_index].length == 1
			_, value = @table[new_index].first
			key, true_value = @true_table[new_index].first
			@table[new_index] = {}
			@true_table[new_index] = {}
			if value >= (2 * true_value)
				@childs[key] = Node.new(nil, nil, child_feature, new_rule_index, key, false)
			else
				@childs[key] = Node.new(nil, nil, child_feature, new_rule_index, key, true)
			end
		else
			@table[new_index].each do |ckey, _|
				child_data = @data.clone
				child_label = @label.clone

				i = 0
				while i < child_data.length
					if child_data[i][new_index] != ckey
						child_data.delete_at(i)
						child_label.delete_at(i)
					else
						child_data[i].delete_at(new_index)
						i += 1
					end
				end
				@childs[ckey] = Node.new(child_data, child_label, child_feature, new_rule_index, ckey)
			end
		end
	end

	def query(data)
		if @flag == nil
			key = data[@rule_index]
			#print(key)

			child =  @childs[key]
			if child == nil
				trys = @childs.map do |_, try|
					try.query(data)
				end
				#print("Meet undefined feature")
				#print(trys)
				if trys.length >= (2 * trys.reduce(:+))
					return false
				else
					return true
				end
			else
				return child.query(data)
			end
		else
			@flag
		end
	end

	def cut
		if @samples >= (2 * @trues)
			@flag = false
		else
			@flag = true
		end
		@_childs = @childs
		@childs = {}
	end

	def commit
		@_childs = nil
	end

	def revert
		@childs = @_childs
		@_childs = nil
		@flag = nil
	end
end

def correct_rate(node, data, label)
	right = (0...label.length).reduce do |sum, i|
		sum + (node.query(data[i]) == label[i])
	end
	#print("Right: #{right}, Total: #{label.length}\n")
	#print("Rate: #{right.to_f / label.length}\n")
	right.to_f / label.length
end

$all_feature = Hash[(0...$train_set.first.length).map { |i| [i, true] }]
$root_node = Node.new($train_set, $train_label, $all_feature)
$best_rate = correct_rate($root_node, $validation_set, $validation_label)

$rates = []
$rates.push([correct_rate($root_node, $train_set, $train_label), $best_rate, correct_rate($root_node, $test_set, $test_label)])

print("Rates: TrainRate, ValidationRate, TestRate\n")
print("Init Best Rate: #{$rates[-1]}\n")

def prune(node, root)
	node.childs.each do |child|
		if child.childs.length > 0
			prune(child, root)
		end
	end

	node.cut

	rate = correct_rate(root, $validation_set, $validation_label)

	if rate >= $best_rate
		node.commit
		$best_rate = rate
		$rates.push([correct_rate(root, $train_set, $train_label), $best_rate, correct_rate(root, $test_set, $test_label)])
		print("Best Rate: #{$rates[-1]}\n")
	else
		node.revert
	end
end

prune($root_node, $root_node)
print("Final Best Rate: #{correct_rate($root_node, $train_set, $train_label)}, #{$best_rate}, #{correct_rate($root_node, $test_set, $test_label)}")

File.open('result.json', 'w') do |f|
	f.syswrite(JSON.generate($rates))
end
