import pytest
from src.telemetry.infrastructure.obd_parser import OBDParser
from src.telemetry.domain.entities import OBDRawFrame
from src.telemetry.domain.value_objects import PIDCode, SessionId
from src.telemetry.domain.exceptions import UnknownPIDError

def test_parser_decodes_rpm():
    parser = OBDParser()
    # RPM is 010C. Formula is (A*256 + B)/4. If A=0x1A (26), B=0x22 (34), RPM = (6656 + 34)/4 = 1672.5
    frame = OBDRawFrame(pid=PIDCode("010C"), raw_bytes=(26, 34))
    decoded = parser.parse(frame, SessionId("test-session"))
    
    assert decoded.label == "Engine RPM"
    assert decoded.value.raw == 1672.5
    assert decoded.value.unit == "RPM"
    assert decoded.session_id.value == "test-session"

def test_parser_unknown_pid():
    parser = OBDParser()
    frame = OBDRawFrame(pid=PIDCode("9999"), raw_bytes=(0,))
    with pytest.raises(UnknownPIDError):
        parser.parse(frame, SessionId("test-session"))
