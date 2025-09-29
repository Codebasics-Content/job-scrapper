from unittest.mock import patch


def _run_main_with_result(result):
    from scrapers.main_wrapper import main_runner

    class DummyApp:
        async def run_scraping_workflow(self, job_role, target_jobs):
            return result

    with patch.object(main_runner, "JobScrapperApplication", return_value=DummyApp()):
        main_runner.main()


def test_main_runner_success(capsys):
    fake_result = {
        "collected_jobs": 25,
        "stored_jobs": 20,
        "statistics": {"skill_percentages": {"python": 100.0}},
    }

    _run_main_with_result(fake_result)

    captured = capsys.readouterr()
    assert "SCRAPING COMPLETE" in captured.out
    assert "Jobs Collected: 25" in captured.out
    assert "Jobs Stored: 20" in captured.out


def test_main_runner_failure(capsys):
    _run_main_with_result(None)

    captured = capsys.readouterr()
    assert "SCRAPING FAILED" in captured.out
