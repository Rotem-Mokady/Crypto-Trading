from bll import Processor


def run() -> None:
    input("Press anything to start")
    processor = Processor()

    try:
        processor.run()
        print(f"Finish Successfully! You can view the results here: {processor.exported_filename}")

    except Exception as e:
        print(f"an error occurred - {repr(e)}")

    input("Press anything to exit")


if __name__ == '__main__':
    run()
