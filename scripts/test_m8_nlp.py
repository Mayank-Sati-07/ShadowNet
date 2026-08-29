from src.nlp.pipeline import CNASFIRPipeline


def main():

    pipeline = CNASFIRPipeline()

    try:

        result = pipeline.process(
            "data/documents/sample_fir.txt"
        )

        print("\n" + "=" * 70)
        print("FINAL EXTRACTION")
        print("=" * 70)

        print(
            result.model_dump_json(
                indent=4
            )
        )

    finally:

        pipeline.close()


if __name__ == "__main__":
    main()
