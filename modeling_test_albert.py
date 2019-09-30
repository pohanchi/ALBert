# coding=utf-8
# export AUTOGRAPH_VERBOSITY=10
# Copyright 2018 The Google AI Language Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import json
import random
import re
import numpy as np
import pdb 
import modeling_albert
import six
import tensorflow as tf
from tensorflow.python.client import timeline
# import tensorboard 
# from tensorboard import 

class ALBertModelTest(tf.test.TestCase):

  class ALBertModelTester(object):

    def __init__(self,
                 parent,
                 batch_size=32,
                 seq_length=512,
                 is_training=True,
                 use_input_mask=True,
                 use_token_type_ids=True,
                 vocab_size=30522,
                 hidden_size=2048,
                 num_hidden_layers=12,
                 num_attention_heads=64,
                 intermediate_size=3072,
                 hidden_act="gelu",
                 hidden_dropout_prob=0.1,
                 attention_probs_dropout_prob=0.1,
                 max_position_embeddings=512,
                 type_vocab_size=2,
                 initializer_range=0.02,
                 scope=None):
      self.parent = parent
      self.batch_size = batch_size
      self.seq_length = seq_length
      self.is_training = is_training
      self.use_input_mask = use_input_mask
      self.use_token_type_ids = use_token_type_ids
      self.vocab_size = vocab_size
      self.hidden_size = hidden_size
      self.num_hidden_layers = num_hidden_layers
      self.num_attention_heads = num_attention_heads
      self.intermediate_size = intermediate_size
      self.hidden_act = hidden_act
      self.hidden_dropout_prob = hidden_dropout_prob
      self.attention_probs_dropout_prob = attention_probs_dropout_prob
      self.max_position_embeddings = max_position_embeddings
      self.type_vocab_size = type_vocab_size
      self.initializer_range = initializer_range
      self.scope = scope

    def create_model(self):
      input_ids = ALBertModelTest.ids_tensor([self.batch_size, self.seq_length],
                                           self.vocab_size)

      input_mask = None
      if self.use_input_mask:
        input_mask = ALBertModelTest.ids_tensor(
            [self.batch_size, self.seq_length], vocab_size=2)

      token_type_ids = None
      if self.use_token_type_ids:
        token_type_ids = ALBertModelTest.ids_tensor(
            [self.batch_size, self.seq_length], self.type_vocab_size)

      config = modeling_albert.ALBertConfig(
          vocab_size=self.vocab_size,
          hidden_size=self.hidden_size,
          num_hidden_layers=self.num_hidden_layers,
          num_attention_heads=self.num_attention_heads,
          intermediate_size=self.intermediate_size,
          hidden_act=self.hidden_act,
          hidden_dropout_prob=self.hidden_dropout_prob,
          attention_probs_dropout_prob=self.attention_probs_dropout_prob,
          max_position_embeddings=self.max_position_embeddings,
          type_vocab_size=self.type_vocab_size,
          initializer_range=self.initializer_range)

      model = modeling_albert.ALBertModel(
          config=config,
          is_training=self.is_training,
          input_ids=input_ids,
          input_mask=input_mask,
          token_type_ids=token_type_ids,
          scope=self.scope)

      outputs = {
          "embedding_output": model.get_embedding_output(),
          "sequence_output": model.get_sequence_output(),
          "pooled_output": model.get_pooled_output(),
          "all_encoder_layers": model.get_all_encoder_layers(),
      }
      print("output: ",outputs["embedding_output"])
      return outputs

    def check_output(self, result):
      self.parent.assertAllEqual(
          result["embedding_output"].shape,
          [self.batch_size, self.seq_length, self.hidden_size])

      self.parent.assertAllEqual(
          result["sequence_output"].shape,
          [self.batch_size, self.seq_length, self.hidden_size])

      self.parent.assertAllEqual(result["pooled_output"].shape,
                                 [self.batch_size, self.hidden_size])

  def test_default(self):
    self.run_tester(ALBertModelTest.ALBertModelTester(self))

  def test_config_to_json_string(self):
    config = modeling_albert.ALBertConfig(vocab_size=30288, hidden_size=2048)
    obj = json.loads(config.to_json_string())
    self.assertEqual(obj["vocab_size"], 30288)
    self.assertEqual(obj["hidden_size"], 2048)

  def run_tester(self, tester):
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.9)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options,log_device_placement=True))
    ops = tester.create_model()
    init_op = tf.group(tf.compat.v1.global_variables_initializer(),
                        tf.compat.v1.local_variables_initializer())
    answer=np.sum([np.prod(v.shape) for v in tf.compat.v1.trainable_variables()])
    run_options = tf.compat.v1.RunOptions(trace_level=tf.compat.v1.RunOptions.FULL_TRACE)
    run_metadata = tf.compat.v1.RunMetadata()
    print("total number:",answer)
    pdb.set_trace()
    sess.run(init_op)
    train_writer = tf.compat.v1.summary.FileWriter('./train_albert', sess.graph)
    output_result = sess.run(ops,options=run_options,run_metadata=run_metadata)
    train_writer.add_run_metadata(run_metadata, 'step%03d' % 0)
    print('Adding run metadata for', 0)
    tl = timeline.Timeline(run_metadata.step_stats)
    print(tl.generate_chrome_trace_format(show_memory=True))
    trace_file = tf.gfile.Open(name='timeline', mode='w')
    trace_file.write(tl.generate_chrome_trace_format(show_memory=True))
    pdb.set_trace()
    tester.check_output(output_result)

    self.assert_all_tensors_reachable(sess, [init_op, ops])


  @classmethod
  def ids_tensor(cls, shape, vocab_size, rng=None, name=None):
    """Creates a random int32 tensor of the shape within the vocab size."""
    if rng is None:
      rng = random.Random()

    total_dims = 1
    for dim in shape:
      total_dims *= dim

    values = []
    for _ in range(total_dims):
      values.append(rng.randint(0, vocab_size - 1))

    return tf.constant(value=values, dtype=tf.int32, shape=shape, name=name)

  def assert_all_tensors_reachable(self, sess, outputs):
    """Checks that all the tensors in the graph are reachable from outputs."""
    graph = sess.graph

    ignore_strings = [
        "^.*/assert_less_equal/.*$",
        "^.*/dilation_rate$",
        "^.*/Tensordot/concat$",
        "^.*/Tensordot/concat/axis$",
        "^testing/.*$",
    ]

    ignore_regexes = [re.compile(x) for x in ignore_strings]

    unreachable = self.get_unreachable_ops(graph, outputs)
    filtered_unreachable = []
    for x in unreachable:
      do_ignore = False
      for r in ignore_regexes:
        m = r.match(x.name)
        if m is not None:
          do_ignore = True
      if do_ignore:
        continue
      filtered_unreachable.append(x)
    unreachable = filtered_unreachable

    self.assertEqual(
        len(unreachable), 0, "The following ops are unreachable: %s" %
        (" ".join([x.name for x in unreachable])))

  @classmethod
  def get_unreachable_ops(cls, graph, outputs):
    """Finds all of the tensors in graph that are unreachable from outputs."""
    outputs = cls.flatten_recursive(outputs)
    output_to_op = collections.defaultdict(list)
    op_to_all = collections.defaultdict(list)
    assign_out_to_in = collections.defaultdict(list)

    for op in graph.get_operations():
      for x in op.inputs:
        op_to_all[op.name].append(x.name)
      for y in op.outputs:
        output_to_op[y.name].append(op.name)
        op_to_all[op.name].append(y.name)
      if str(op.type) == "Assign":
        for y in op.outputs:
          for x in op.inputs:
            assign_out_to_in[y.name].append(x.name)

    assign_groups = collections.defaultdict(list)
    for out_name in assign_out_to_in.keys():
      name_group = assign_out_to_in[out_name]
      for n1 in name_group:
        assign_groups[n1].append(out_name)
        for n2 in name_group:
          if n1 != n2:
            assign_groups[n1].append(n2)

    seen_tensors = {}
    stack = [x.name for x in outputs]
    while stack:
      name = stack.pop()
      if name in seen_tensors:
        continue
      seen_tensors[name] = True

      if name in output_to_op:
        for op_name in output_to_op[name]:
          if op_name in op_to_all:
            for input_name in op_to_all[op_name]:
              if input_name not in stack:
                stack.append(input_name)

      expanded_names = []
      if name in assign_groups:
        for assign_name in assign_groups[name]:
          expanded_names.append(assign_name)

      for expanded_name in expanded_names:
        if expanded_name not in stack:
          stack.append(expanded_name)

    unreachable_ops = []
    for op in graph.get_operations():
      is_unreachable = False
      all_names = [x.name for x in op.inputs] + [x.name for x in op.outputs]
      for name in all_names:
        if name not in seen_tensors:
          is_unreachable = True
      if is_unreachable:
        unreachable_ops.append(op)
    return unreachable_ops

  @classmethod
  def flatten_recursive(cls, item):
    """Flattens (potentially nested) a tuple/dictionary/list to a list."""
    output = []
    if isinstance(item, list):
      output.extend(item)
    elif isinstance(item, tuple):
      output.extend(list(item))
    elif isinstance(item, dict):
      for (_, v) in six.iteritems(item):
        output.append(v)
    else:
      return [item]

    flat_output = []
    for x in output:
      flat_output.extend(cls.flatten_recursive(x))
    return flat_output


if __name__ == "__main__":
  with tf.device("/device:GPU:0"):
    tf.test.main()
