
require "socket"

PYTHON   = "python3"
HOSTNAME = Socket.gethostname

file "tmp/categorized_rail.msgpack" => ["../data/ironnews/rail.txt"] do |t|
  sh("time", PYTHON, "-u", "../1_collect.py", "rail", *(t.prerequisites + [t.name]))
end

file "tmp/categorized_other.msgpack" => ["../data/ironnews/other.txt"] do |t|
  sh("time", PYTHON, "-u", "../1_collect.py", "other", *(t.prerequisites + [t.name]))
end

file "tmp/categorized.msgpack" => ["tmp/categorized_rail.msgpack", "tmp/categorized_other.msgpack"] do |t|
  sh("time", PYTHON, "-u", "../2_merge.py", *(t.prerequisites + [t.name]))
end

file "tmp/tokenized.msgpack" => ["tmp/categorized.msgpack"] do |t|
  sh("time", PYTHON, "-u", "../3_tokenize.py", *(t.prerequisites + [t.name]))
end

file "tmp/dictionary.msgpack" => ["tmp/tokenized.msgpack"] do |t|
  sh("time", PYTHON, "-u", "../4_make_dictionary.py", *(t.prerequisites + [t.name]))
end

file "tmp/vectorized.msgpack" => ["tmp/dictionary.msgpack", "tmp/tokenized.msgpack"] do |t|
  sh("time", PYTHON, "-u", "../5_vectorize.py", *(t.prerequisites + [t.name]))
end

task :sample => ["tmp/vectorized.msgpack"] do |t|
  sh("time", PYTHON, "-u", "../6_sample.py", *(t.prerequisites + ["tmp/test.msgpack", "tmp/train.msgpack"]))
end

task :sample_time do |t|
  sh("time rake sample")
end

task :sample_tee do |t|
  logname = "out/#{HOSTNAME}/sample.log"
  mkdir_p(File.dirname(logname))
  sh("date 2>&1 | tee '#{logname}'")
  sh("rake sample_time 2>&1 | tee -a '#{logname}'")
  sh("date 2>&1 | tee -a '#{logname}'")
end

task :train => ["tmp/dictionary.msgpack", "tmp/test.msgpack", "tmp/train.msgpack"] do |t|
  mkdir_p("out/#{HOSTNAME}")
  sh("time", PYTHON, "-u", "../7_train.py", *(t.prerequisites + ["out/#{HOSTNAME}/model", "out/#{HOSTNAME}/data"]))
end

task :train_time do |t|
  sh("time rake train")
end

task :train_tee do |t|
  logname = "out/#{HOSTNAME}/train.log"
  mkdir_p(File.dirname(logname))
  sh("date 2>&1 | tee '#{logname}'")
  sh("rake train_time 2>&1 | tee -a '#{logname}'")
  sh("date 2>&1 | tee -a '#{logname}'")
end

task :prediction => ["tmp/dictionary.msgpack", "out/#{HOSTNAME}/model"] do |t|
  sh("time", PYTHON, "-u", "../8_prediction.py", *t.prerequisites)
end

task :clean do |t|
  rm_f(FileList["tmp/*.msgpack"])
  rm_f(FileList["data/*.#{HOSTNAME}"])
  rm_rf("out/#{HOSTNAME}")
end
