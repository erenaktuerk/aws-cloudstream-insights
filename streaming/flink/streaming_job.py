from pyflink.datastream import StreamExecutionEnvironment

env = StreamExecutionEnvironment.get_execution_environment()

def process(event):
    return event

env.execute("cloudstream-streaming-job")