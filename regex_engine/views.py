from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .engine import get_all_patterns, get_pattern, validate_string, match_natural_language


@api_view(['GET'])
def list_patterns(request):
    """List all available RE patterns."""
    return Response(get_all_patterns())


@api_view(['GET'])
def pattern_detail(request, key):
    """Get full detail for a specific pattern."""
    pattern = get_pattern(key)
    if not pattern:
        return Response({"error": f"Pattern '{key}' not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response({**pattern, "key": key})


@api_view(['POST'])
def validate(request):
    """
    Validate a binary string against a pattern.
    Body: { "key": "starts_with_0_ends_with_1", "input": "0101" }
    """
    key = request.data.get("key")
    binary_input = request.data.get("input", "")

    if not key:
        return Response({"error": "Field 'key' is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Validate input is binary
    if binary_input and not all(c in '01' for c in binary_input):
        return Response({"error": "Input must only contain 0s and 1s."}, status=status.HTTP_400_BAD_REQUEST)

    result = validate_string(key, binary_input)
    if "error" in result:
        return Response(result, status=status.HTTP_404_NOT_FOUND)
    return Response(result)


@api_view(['POST'])
def nlp_match(request):
    """
    Match a natural language description to a Regular Expression.
    Body: { "text": "All binary strings that do not contain 11 as a substring" }
    """
    text = request.data.get("text", "").strip()
    if not text:
        return Response({"error": "Field 'text' is required."}, status=status.HTTP_400_BAD_REQUEST)

    result = match_natural_language(text)
    return Response(result)
